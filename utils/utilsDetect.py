# %%
import cv2
import math
from PIL import Image
import time
from utils.utilsXml import saveXml
from classdir.DetectInfo import DetectInfo


def getNowTime():
    return time.strftime('_D%Y%m%d_T%H%M%S', time.localtime())

# %%
# 图像切割
def cutImage(imgPath,                    # 图像存储位置
            outShape):                  # 切割后图像形状
    img = cv2.imread(imgPath)           # 打开图像
    h, w, d = img.shape                  # 获取图像的高,宽,通道数
    widthCol = math.ceil(w / outShape[0])  # 列
    heightRow = math.ceil(h / outShape[1])  # 行
    # 扩展图像(0填充)
    img = cv2.copyMakeBorder(img, 0, heightRow * outShape[1] - h,
                             0, widthCol * outShape[0] - w, 
                             cv2.BORDER_CONSTANT, value=0)
    # 分割图像，将其存入list中
    outImage = []
    for i in range(heightRow):
        tmp = []
        heightStart = i * outShape[1]
        for j in range(widthCol):
            widthStart = j * outShape[0]
            eachImage = img[heightStart:(heightStart + outShape[1]), 
                           widthStart:( widthStart + outShape[0])]
            # 存入list中的图像格式为PIL.Iamge, 因此需要进行色彩空间的转换
            tmp.append(Image.fromarray(cv2.cvtColor(eachImage, cv2.COLOR_BGR2RGB)))
        outImage.append(tmp)
    return outImage, w, h, d
    
# %%
# 图像识别
def detectImage(imgPath,            # 图像存储路径
           imgName,            # 图像名字
           imgShape,           # 识别时图像形状
           model,               # yolo模型
           xmlPath,            # xml保存路径
           dictClass):         # 瑕疵类型字典
    # 图像切割
    image, w, h, d = cutImage(imgPath + imgName, imgShape)
    # 
    info = DetectInfo(imgPath, imgName, w, h, d)
    # 瑕疵检测
    for i in range(len(image)):
        for j in range(len(image[i])):
            box, score, classes = model.detectImage(image[i][j])
            for k in range(len(box)):
                info.addFlaw([int(box[k][1] + imgShape[0] * j), int(box[k][0] + imgShape[1] * i), 
                    math.ceil(box[k][3] + imgShape[0] * j), math.ceil(box[k][2] + imgShape[1] * i), 
                    score[k], dictClass[classes[k]]])
    # 设置检测时间
    info.updateTime(getNowTime())
    # 保存检测信息
    saveXml(info, xmlPath)
    return info

def draw(info,              # 检测信息
         colordist):        # 颜色字典
    img = cv2.imread(info.path + info.name)
    for i in info.flawList:
        # 画框
        img = cv2.rectangle(img, (i[0], i[1]), (i[2], i[3]), colordist[i[5]], 2)
    return img