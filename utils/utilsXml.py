from xml.dom.minidom import Document
import xml.etree.ElementTree as ET
from classdir.DetectInfo import DetectInfo

# 将检测信息保存为xml
def saveXml(detectInfo, xmlPath):
    name = detectInfo.name[:-4]
    xmlBuilder = Document()
    annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
    xmlBuilder.appendChild(annotation)
    filename = xmlBuilder.createElement("filename")  # filename标签
    filenamecontent = xmlBuilder.createTextNode(name + ".jpg")
    filename.appendChild(filenamecontent)
    annotation.appendChild(filename)  # filename标签结束
    filepath = xmlBuilder.createElement("filepath")  # filepath标签
    filepathcontent = xmlBuilder.createTextNode(detectInfo.path)
    filepath.appendChild(filepathcontent)
    annotation.appendChild(filepath)  # filepath标签结束
    detecttime = xmlBuilder.createElement("detecttime") # detecttime标签
    detecttimecontent = xmlBuilder.createTextNode(detectInfo.detectTime)
    detecttime.appendChild(detecttimecontent)
    annotation.appendChild(detecttime)  # detecttime标签结束
    size = xmlBuilder.createElement("size")  # size标签
    width = xmlBuilder.createElement("width")  # size子标签width
    widthcontent = xmlBuilder.createTextNode(str(detectInfo.width))
    width.appendChild(widthcontent)
    size.appendChild(width)  # size子标签width结束
    height = xmlBuilder.createElement("height")  # size子标签height
    heightcontent = xmlBuilder.createTextNode(str(detectInfo.height))
    height.appendChild(heightcontent)
    size.appendChild(height)  # size子标签height结束
    depth = xmlBuilder.createElement("depth")  # size子标签depth
    depthcontent = xmlBuilder.createTextNode(str(detectInfo.depth))
    depth.appendChild(depthcontent)
    size.appendChild(depth)  # size子标签depth结束
    annotation.appendChild(size)  # size标签结束
    for i in detectInfo.flawList:
        object = xmlBuilder.createElement("object")  # object 标签
        score = xmlBuilder.createElement("score")  # score标签
        scoreContent = xmlBuilder.createTextNode(str(i[4]))
        score.appendChild(scoreContent)
        object.appendChild(score)  # score标签结束
        classes = xmlBuilder.createElement("name")  # name标签
        classesContent = xmlBuilder.createTextNode(i[5])
        classes.appendChild(classesContent)
        object.appendChild(classes)  # classes标签结束
        bndbox = xmlBuilder.createElement("bndbox")  # bndbox标签
        xmin = xmlBuilder.createElement("xmin")  # xmin标签
        xminContent = xmlBuilder.createTextNode(str(i[0]))
        xmin.appendChild(xminContent)
        bndbox.appendChild(xmin)  # xmin标签结束
        ymin = xmlBuilder.createElement("ymin")  # ymin标签
        yminContent = xmlBuilder.createTextNode(str(i[1]))
        ymin.appendChild(yminContent)
        bndbox.appendChild(ymin)  # ymin标签结束
        xmax = xmlBuilder.createElement("xmax")  # xmax标签
        xmaxContent = xmlBuilder.createTextNode(str(i[2]))
        xmax.appendChild(xmaxContent)
        bndbox.appendChild(xmax)  # xmax标签结束
        ymax = xmlBuilder.createElement("ymax")  # ymax标签
        ymaxContent = xmlBuilder.createTextNode(str(i[3]))
        ymax.appendChild(ymaxContent)
        bndbox.appendChild(ymax)  # ymax标签结束
        object.appendChild(bndbox)  # bndbox标签结束
        annotation.appendChild(object)  # object标签结束
    f = open(xmlPath + name +  detectInfo.detectTime + ".xml", 'w')
    xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
    f.close()
    
# 解析xml文件
def analyzeXml(xmlpath):
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    imageShape = root.find('size')
    info = DetectInfo(root.find('filepath').text,
        root.find('filename').text, imageShape.find('width').text,
        imageShape.find('height').text, imageShape.find('depth').text)
    info.updateTime(root.find('detecttime').text)
    for obj in root.iter('object'):
        bbox = obj.find('bndbox')
        info.addFlaw([int(bbox.find('xmin').text), 
                      int(bbox.find('ymin').text),
                      int(bbox.find('xmax').text), 
                      int(bbox.find('ymax').text),
                      float(obj.find('score').text), 
                      obj.find('name').text])
    return info

# 将字符串转换为元组
def toTuple(s):
    tmp = s.replace('(','').replace(')','')
    return tuple([int(i) for i in tmp.split(',')])

# 加载并解析配置文件
def loadConfig():
    # 默认配置信息
    configDict = {
        'modelPath': "model/",
        'imageShape': [832.608],
        'confidence': 0.5,
        'nms_iou': 0.3,
        'maxBoxes': 100,
        'letterboxImage': False,
        'detectAnsDir': 'detectAns',
        'color': {
            "edge anomaly": (238, 238, 0),
            "corner anomaly": (0, 255, 0),
            "white point blemishes": (0, 255, 255),
            "light block blemishes": (0, 0, 255),
            "dark spot blemishes": (226, 43, 138),
            "aperture blemishes": (98, 28, 139)}}
    try:
        tree = ET.parse('config.xml')
    except FileNotFoundError:
        return configDict
    root = tree.getroot()
    imageShape = tree.find('imageShape')
    configDict['modelPath']      = root.find('modelPath').text
    configDict['imageShape']     = [int(imageShape.find('width').text), int(imageShape.find('height').text)]
    configDict['confidence']     = float(root.find('confidence').text)
    configDict['nms_iou']        = float(root.find('nms_iou').text)
    configDict['maxBoxes']       = int(root.find('maxBoxes').text)
    configDict['letterboxImage'] = bool(root.find('letterboxImage').text)
    configDict['detectAnsDir']   = root.find('detectAnsDir').text
    configDict['color']['edge anomaly'] = toTuple(root.find('edge_anomaly').text)
    configDict['color']['corner anomaly'] = toTuple(root.find('corner_anomaly').text)
    configDict['color']['white point blemishes'] = toTuple(root.find('white_point_blemishes').text)
    configDict['color']['light block blemishes'] = toTuple(root.find('light_block_blemishes').text)
    configDict['color']['dark spot blemishes'] = toTuple(root.find('dark_spot_blemishes').text)
    configDict['color']['aperture blemishes'] = toTuple(root.find('aperture_blemishes').text)
    print(configDict)
    return configDict
        