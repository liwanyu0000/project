import tensorflow as tf
from tensorflow.keras.layers import Concatenate, Input, Lambda, UpSampling2D, ZeroPadding2D
from tensorflow.keras.models import Model
from networks.CSPdarknet import C3, DarknetConv2D, DarknetConv2D_BN_SiLU, darknet_body
from tensorflow.keras import backend as Keras
from utils.utilsBbox import get_anchors_and_decode, smooth_labels, box_ciou

#---------------------------------------------------#
#   loss值计算
#---------------------------------------------------#
def yolo_loss(
    args, 
    input_shape, 
    anchors, 
    anchors_mask, 
    num_classes, 
    balance         = [0.4, 1.0, 4], 
    label_smoothing = 0.01, 
    box_ratio       = 0.05, 
    obj_ratio       = 1, 
    cls_ratio       = 0.5
):
    num_layers = len(anchors_mask)
    #---------------------------------------------------------------------------------------------------#
    #   将预测结果和实际ground truth分开，args是[*model_body.output, *y_true]
    #   y_true是一个列表，包含三个特征层，shape分别为:
    #   (m,20,20,3,85)
    #   (m,40,40,3,85)
    #   (m,80,80,3,85)
    #   yolo_outputs是一个列表，包含三个特征层，shape分别为:
    #   (m,20,20,3,85)
    #   (m,40,40,3,85)
    #   (m,80,80,3,85)
    #---------------------------------------------------------------------------------------------------#
    y_true          = args[num_layers:]
    yolo_outputs    = args[:num_layers]

    #-----------------------------------------------------------#
    #   得到input_shpae为416,416 
    #-----------------------------------------------------------#
    input_shape = Keras.cast(input_shape, Keras.dtype(y_true[0]))

    loss    = 0
    #---------------------------------------------------------------------------------------------------#
    #   y_true是一个列表，包含三个特征层，shape分别为(m,20,20,3,85),(m,40,40,3,85),(m,80,80,3,85)。
    #   yolo_outputs是一个列表，包含三个特征层，shape分别为(m,20,20,3,85),(m,40,40,3,85),(m,80,80,3,85)。
    #---------------------------------------------------------------------------------------------------#
    for l in range(num_layers):
        #-----------------------------------------------------------#
        #   以第一个特征层(m,20,20,3,85)为例子
        #   取出该特征层中存在目标的点的位置。(m,20,20,3,1)
        #-----------------------------------------------------------#
        object_mask = y_true[l][..., 4:5]
        #-----------------------------------------------------------#
        #   取出其对应的种类(m,20,20,3,80)
        #-----------------------------------------------------------#
        true_class_probs = y_true[l][..., 5:]
        if label_smoothing:
            true_class_probs = smooth_labels(true_class_probs, label_smoothing)

        #-----------------------------------------------------------#
        #   将yolo_outputs的特征层输出进行处理、获得四个返回值
        #   其中：
        #   grid        (20,20,1,2) 网格坐标
        #   raw_pred    (m,20,20,3,85) 尚未处理的预测结果
        #   pred_xy     (m,20,20,3,2) 解码后的中心坐标
        #   pred_wh     (m,20,20,3,2) 解码后的宽高坐标
        #-----------------------------------------------------------#
        grid, raw_pred, pred_xy, pred_wh = get_anchors_and_decode(yolo_outputs[l],
             anchors[anchors_mask[l]], num_classes, input_shape, calc_loss=True)
        
        #-----------------------------------------------------------#
        #   pred_box是解码后的预测的box的位置
        #   (m,20,20,3,4)
        #-----------------------------------------------------------#
        pred_box = Keras.concatenate([pred_xy, pred_wh])

        #-----------------------------------------------------------#
        #   计算Ciou loss
        #-----------------------------------------------------------#
        raw_true_box    = y_true[l][...,0:4]
        ciou            = box_ciou(pred_box, raw_true_box)
        ciou_loss       = object_mask * (1 - ciou)
        
        #------------------------------------------------------------------------------#
        #   如果该位置本来有框，那么计算1与置信度的交叉熵
        #   如果该位置本来没有框，那么计算0与置信度的交叉熵
        #   在这其中会忽略一部分样本，这些被忽略的样本满足条件best_iou<ignore_thresh
        #   该操作的目的是：
        #   忽略预测结果与真实框非常对应特征点，因为这些框已经比较准了
        #   不适合当作负样本，所以忽略掉。
        #------------------------------------------------------------------------------#
        tobj            = tf.where(tf.equal(object_mask, 1), tf.maximum(ciou, tf.zeros_like(ciou)), tf.zeros_like(ciou))
        confidence_loss = Keras.binary_crossentropy(tobj, raw_pred[..., 4:5], from_logits=True)

        #-----------------------------------------------------------#
        #   计算分类损失
        #-----------------------------------------------------------#
        class_loss      = object_mask * Keras.binary_crossentropy(true_class_probs, raw_pred[...,5:], from_logits=True)

        #-----------------------------------------------------------#
        #   计算正样本数量
        #-----------------------------------------------------------#
        num_pos         = tf.maximum(Keras.sum(Keras.cast(object_mask, tf.float32)), 1)

        location_loss   = Keras.sum(ciou_loss) * box_ratio / num_pos
        confidence_loss = Keras.mean(confidence_loss) * balance[l] * obj_ratio
        class_loss      = Keras.sum(class_loss) * cls_ratio / num_pos / num_classes

        loss    += location_loss + confidence_loss + class_loss
        # if print_loss:
        # loss = tf.Print(loss, [loss, location_loss, confidence_loss, class_loss], message='loss: ')
        
    return loss
#---------------------------------------------------#
#   Panet网络的构建，并且获得预测结果
#---------------------------------------------------#
def yoloBody(input_shape, anchors_mask, num_classes, phi, weight_decay=5e-4):
    depth_dict          = {'s' : 0.33, 'm' : 0.67, 'l' : 1.00, 'x' : 1.33,}
    width_dict          = {'s' : 0.50, 'm' : 0.75, 'l' : 1.00, 'x' : 1.25,}
    dep_mul, wid_mul    = depth_dict[phi], width_dict[phi]

    base_channels       = int(wid_mul * 64)  # 64
    base_depth          = max(round(dep_mul * 3), 1)  # 3

    inputs      = Input(input_shape)
    #---------------------------------------------------#   
    #   生成主干模型，获得三个有效特征层，他们的shape分别是：
    #   80, 80, 256
    #   40, 40, 512
    #   20, 20, 1024
    #---------------------------------------------------#
    feat1, feat2, feat3 = darknet_body(inputs, base_channels, base_depth, weight_decay)

    P5          = DarknetConv2D_BN_SiLU(int(base_channels * 8), (1, 1), weight_decay=weight_decay, name = 'conv_for_feat3')(feat3)  
    P5_upsample = UpSampling2D()(P5) 
    P5_upsample = Concatenate(axis = -1)([P5_upsample, feat2])
    P5_upsample = C3(P5_upsample, int(base_channels * 8), base_depth, shortcut = False, weight_decay=weight_decay, name = 'conv3_for_upsample1')

    P4          = DarknetConv2D_BN_SiLU(int(base_channels * 4), (1, 1), weight_decay=weight_decay, name = 'conv_for_feat2')(P5_upsample)
    P4_upsample = UpSampling2D()(P4)
    P4_upsample = Concatenate(axis = -1)([P4_upsample, feat1])
    P3_out      = C3(P4_upsample, int(base_channels * 4), base_depth, shortcut = False, weight_decay=weight_decay, name = 'conv3_for_upsample2')

    P3_downsample   = ZeroPadding2D(((1, 0),(1, 0)))(P3_out)
    P3_downsample   = DarknetConv2D_BN_SiLU(int(base_channels * 4), (3, 3), strides = (2, 2), weight_decay=weight_decay, name = 'down_sample1')(P3_downsample)
    P3_downsample   = Concatenate(axis = -1)([P3_downsample, P4])
    P4_out          = C3(P3_downsample, int(base_channels * 8), base_depth, shortcut = False, weight_decay=weight_decay, name = 'conv3_for_downsample1') 

    P4_downsample   = ZeroPadding2D(((1, 0),(1, 0)))(P4_out)
    P4_downsample   = DarknetConv2D_BN_SiLU(int(base_channels * 8), (3, 3), strides = (2, 2), weight_decay=weight_decay, name = 'down_sample2')(P4_downsample)
    P4_downsample   = Concatenate(axis = -1)([P4_downsample, P5])
    P5_out          = C3(P4_downsample, int(base_channels * 16), base_depth, shortcut = False, weight_decay=weight_decay, name = 'conv3_for_downsample2')

    out2 = DarknetConv2D(len(anchors_mask[2]) * (5 + num_classes), (1, 1), strides = (1, 1), weight_decay=weight_decay, name = 'yolo_head_P3')(P3_out)
    out1 = DarknetConv2D(len(anchors_mask[1]) * (5 + num_classes), (1, 1), strides = (1, 1), weight_decay=weight_decay, name = 'yolo_head_P4')(P4_out)
    out0 = DarknetConv2D(len(anchors_mask[0]) * (5 + num_classes), (1, 1), strides = (1, 1), weight_decay=weight_decay, name = 'yolo_head_P5')(P5_out)
    return Model(inputs, [out0, out1, out2])

def get_train_model(model_body, input_shape, num_classes, anchors, anchors_mask, label_smoothing):
    y_true = [Input(shape = (input_shape[0] // {0:32, 1:16, 2:8}[l], input_shape[1] // {0:32, 1:16, 2:8}[l], \
                                len(anchors_mask[l]), num_classes + 5)) for l in range(len(anchors_mask))]
    model_loss  = Lambda(
        yolo_loss, 
        output_shape    = (1, ), 
        name            = 'yolo_loss', 
        arguments       = {
            'input_shape'       : input_shape, 
            'anchors'           : anchors, 
            'anchors_mask'      : anchors_mask, 
            'num_classes'       : num_classes, 
            'label_smoothing'   : label_smoothing, 
            'balance'           : [0.4, 1.0, 4],
            'box_ratio'         : 0.05,
            'obj_ratio'         : 1 * (input_shape[0] * input_shape[1]) / (640 ** 2), 
            'cls_ratio'         : 0.5 * (num_classes / 80)
        }
    )([*model_body.output, *y_true])
    model       = Model([model_body.input, *y_true], model_loss)
    return model
