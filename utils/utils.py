from functools import reduce
import numpy as np
from PIL import Image


def compose(*funcs):
    if funcs:
        return reduce(lambda f, g: lambda *a, **kw: g(f(*a, **kw)), funcs)
    else:
        raise ValueError('Composition of empty sequence not supported.')

#---------------------------------------------------------#
#   将图像转换成RGB图像，防止灰度图在预测时报错。
#   代码仅仅支持RGB图像的预测，所有其它类型的图像都会转化成RGB
#---------------------------------------------------------#
def cvtColor(image):
    if len(np.shape(image)) == 3 and np.shape(image)[2] == 3:
        return image 
    else:
        image = image.convert('RGB')
        return image 

#---------------------------------------------------#
#   对输入图像进行resize
#---------------------------------------------------#
def resizeImage(image, size, letterBoxImage):
    iw, ih  = image.size
    w, h    = size
    if letterBoxImage:
        scale   = min(w / iw, h / ih)
        nw      = int(iw * scale)
        nh      = int(ih * scale)
        image   = image.resize((nw,nh), Image.BICUBIC)
        newImage = Image.new('RGB', size, (128,128,128))
        newImage.paste(image, ((w - nw) // 2, (h - nh) // 2))
    else:
        newImage = image.resize((w, h), Image.BICUBIC)
    return newImage

#---------------------------------------------------#
#   获得类
#---------------------------------------------------#
def getClasses(classesPath):
    with open(classesPath, encoding='utf-8') as f:
        classNames = f.readlines()
    classNames = [c.strip() for c in classNames]
    return classNames, len(classNames)

#---------------------------------------------------#
#   获得先验框
#---------------------------------------------------#
def getAnchors(anchorsPath):
    '''loads the anchors from a file'''
    with open(anchorsPath, encoding='utf-8') as f:
        anchors = f.readline()
    anchors = [float(x) for x in anchors.split(',')]
    anchors = np.array(anchors).reshape(-1, 2)
    return anchors, len(anchors)

def preprocessInput(image):
    image /= 255.0
    return image