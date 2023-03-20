# import colorsys
import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Input, Lambda
from tensorflow.keras.models import Model
from networks.yolo import yoloBody
from utils.utils import cvtColor, getAnchors, getClasses, preprocessInput, resizeImage
from utils.utilsBbox import DecodeBox


class YOLO(object):
    # anchorsPath代表先验框对应的txt文件，一般不修改。
    _anchorsPath = 'model/yolo_anchors.txt'
    # anchorsMask用于帮助代码找到对应的先验框，一般不修改
    _anchorsMask = [[6, 7, 8], [3, 4, 5], [0, 1, 2]]
    _classesPath = 'model/cls_classes.txt'
    # 权重文件路径
    _modelPath = 'model/yolov5_best_weights_s.h5'
    # 设置yolov5版本
    _phi = 's'
    # 设置置信度
    _confidence = 0.5
    # 非极大抑制所用到的nms_iou大小
    _nms_iou = 0.3
    # 最大框的数量
    _maxBoxes = 100
    # 该变量用于控制是否使用letterbox_image对输入图像进行不失真的resize
    _letterboxImage = False
    # 初始化yolo
    def __init__(self, inputShape):
        # 设置输入图像的形状
        self._inputShape = inputShape
        # 获得种类和先验框的数量
        self._classNames, self._numClasses = getClasses(self._classesPath)
        self._anchors, self._numAnchors    = getAnchors(self._anchorsPath)
        # 载入模型
        self.generate()

    #  载入模型
    def generate(self):
        modelPath = os.path.expanduser(self._modelPath)
        assert modelPath.endswith('.h5'), 'Keras model or weights must be a .h5 file.'
        self.model = yoloBody([None, None, 3], self._anchorsMask, self._numClasses, self._phi)
        self.model.load_weights(self._modelPath)
        #  在DecodeBox函数中，我们会对预测结果进行后处理
        #  后处理的内容包括，解码、非极大抑制、门限筛选等
        self.input_image_shape = Input([2,],batch_size=1)
        inputs  = [*self.model.output, self.input_image_shape]
        outputs = Lambda(
            DecodeBox, 
            output_shape = (1,), 
            name = 'yolo_eval',
            arguments = {
                'anchors'           : self._anchors, 
                'num_classes'       : self._numClasses, 
                'input_shape'       : self._inputShape, 
                'anchor_mask'       : self._anchorsMask,
                'confidence'        : self._confidence, 
                'nms_iou'           : self._nms_iou, 
                'max_boxes'         : self._maxBoxes, 
                'letterbox_image'   : self._letterboxImage
             }
        )(inputs)
        self.yoloModel = Model([self.model.input, self.input_image_shape], outputs)

    @tf.function
    def get_pred(self, imageData, inputImageShape):
        outBoxes, outScores, outClasses = self.yoloModel([imageData, inputImageShape], training=False)
        return outBoxes, outScores, outClasses
    
    #  检测图片
    def detectImage(self, image):
        #  在这里将图像转换成RGB图像，防止灰度图在预测时报错。
        #  代码仅仅支持RGB图像的预测，所有其它类型的图像都会转化成RGB
        image       = cvtColor(image)
        #  给图像增加灰条，实现不失真的resize
        #  也可以直接resize进行识别
        image_data  = resizeImage(image, (self._inputShape[1], self._inputShape[0]), self._letterboxImage)
        #  添加上batch_size维度，并进行归一化
        image_data  = np.expand_dims(preprocessInput(np.array(image_data, dtype='float32')), 0)
        #  将图像输入网络当中进行预测
        inputImageShape = np.expand_dims(np.array([image.size[1], image.size[0]], dtype='float32'), 0)
        outBoxes, outScores, outClasses = self.get_pred(image_data, inputImageShape) 
        return outBoxes.numpy(), outScores.numpy() , outClasses.numpy()
    
    # 修改权重文件路径
    def setModelPath(self, modelPath, phi):
        self._modelPath = modelPath
        self._phi = phi
        # 重新载入模型
        self.generate()
    
    # 修改输入图像形状
    def setInputShape(self, inputShape):
        self._inputShape = inputShape  
        # 重新载入模型
        self.generate()
    
    # 修改Yolo相关参数
    def setYolo(self, **kwargs):
        for key, vaule in kwargs.items():
            # 修改非极大抑制所用到的nms_iou
            if key == 'nms_iou':
                self._nms_iou = vaule
            # 修改最大框数量
            elif key == 'maxBoxes':
                self._maxBoxes = vaule
            # 修改否使用letterbox_image对输入图像进行不失真的resize
            elif key == 'letterboxImage':
                self._letterboxImage = vaule
            # 修改输入图像形状
            elif key == 'inputShape':
                self._inputShape = vaule
            # 修改先验框文件路径
            if key == 'anchorsPath':
                self._anchorsPath = vaule
                self._anchors, self._numAnchors = getAnchors(self._anchorsPath)
            # 修改瑕疵类型文件路径
            elif key == 'classesPath':
                self._classesPath = vaule
                self._classNames, self._numClasses = getClasses(self._classesPath)
            # 修改先验框对应位置
            elif key == 'anchorsMask':
                self._anchorsMask = vaule
            # 修改置信度
            elif key == 'confidence':
                self._confidence = vaule
            else:
                continue      
        # 重新载入模型
        self.generate()
        
