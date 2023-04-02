try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from xml.dom.minidom import Document
from classdir.DetectInfo import DetectInfo
import datetime

# 将检测信息保存为xml
def saveXml(detectInfo, xmlPath):
    name = detectInfo.path.split('/')[-1].split('.')[0]
    xmlBuilder = Document()
    annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
    xmlBuilder.appendChild(annotation)
    filename = xmlBuilder.createElement("filename")  # filename标签
    filenamecontent = xmlBuilder.createTextNode(detectInfo.path)
    filename.appendChild(filenamecontent)
    annotation.appendChild(filename)  # filename标签结束
    # filepath = xmlBuilder.createElement("filepath")  # filepath标签
    # filepathcontent = xmlBuilder.createTextNode(detectInfo.path)
    # filepath.appendChild(filepathcontent)
    # annotation.appendChild(filepath)  # filepath标签结束
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
    tmptime = datetime.datetime.strptime(detectInfo.detectTime, "%Y-%m-%d %H:%M:%S")
    f = open(xmlPath + name +  tmptime.strftime("_D%Y%m%d_T%H%M%S") + ".xml", 'w')
    xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
    f.close()
    
# 解析xml文件
def analyzeXml(xmlpath):
    tree = ET.parse(xmlpath)
    root = tree.getroot()
    imageShape = root.find('size')
    info = DetectInfo(root.find('filename').text, imageShape.find('width').text,
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

# 写配置文件
def writeConfig(configInfo):
    xmlBuilder = Document()
    annotation = xmlBuilder.createElement("annotation")  # 创建annotation标签
    xmlBuilder.appendChild(annotation)
    modelPath = xmlBuilder.createElement("modelPath")  # modelPath标签
    modelPathContent = xmlBuilder.createTextNode(str(configInfo['modelPath']))
    modelPath.appendChild(modelPathContent)
    annotation.appendChild(modelPath)          #modelPath标签结束
    imageShape = xmlBuilder.createElement("imageShape")  # imageShape标签
    width = xmlBuilder.createElement("width")  # imageShape子标签width
    widthcontent = xmlBuilder.createTextNode(str(configInfo['imageShape'][0]))
    width.appendChild(widthcontent)
    imageShape.appendChild(width)  # imageShape子标签width结束
    height = xmlBuilder.createElement("height")  # imageShape子标签height
    heightcontent = xmlBuilder.createTextNode(str(configInfo['imageShape'][1]))
    height.appendChild(heightcontent)
    imageShape.appendChild(height)  # imageShape子标签height结束
    annotation.appendChild(imageShape)          #imageShape标签结束
    confidence = xmlBuilder.createElement("confidence")  # confidence标签
    confidenceContent = xmlBuilder.createTextNode(str(configInfo['confidence']))
    confidence.appendChild(confidenceContent)
    annotation.appendChild(confidence)          #confidence标签结束
    nms_iou = xmlBuilder.createElement("nms_iou")  # nms_iou标签
    nms_iouContent = xmlBuilder.createTextNode(str(configInfo['nms_iou']))
    nms_iou.appendChild(nms_iouContent)
    annotation.appendChild(nms_iou)          #nms_iou标签结束
    maxBoxes = xmlBuilder.createElement("maxBoxes")  # maxBoxes标签
    maxBoxesContent = xmlBuilder.createTextNode(str(configInfo['maxBoxes']))
    maxBoxes.appendChild(maxBoxesContent)
    annotation.appendChild(maxBoxes)          #maxBoxes标签结束
    letterboxImage = xmlBuilder.createElement("letterboxImage")  # letterboxImage标签
    letterboxImageContent = xmlBuilder.createTextNode(str(configInfo['letterboxImage']))
    letterboxImage.appendChild(letterboxImageContent)
    annotation.appendChild(letterboxImage)          #letterboxImage标签结束
    detectAnsPath = xmlBuilder.createElement("detectAnsPath")  # detectAnsPath标签
    detectAnsPathContent = xmlBuilder.createTextNode(str(configInfo['detectAnsPath']))
    detectAnsPath.appendChild(detectAnsPathContent)
    annotation.appendChild(detectAnsPath)          #detectAnsPath标签结束
    edge_anomaly = xmlBuilder.createElement("edge_anomaly")  # edge_anomaly标签
    edge_anomalyContent = xmlBuilder.createTextNode(str(configInfo['color']['edge_anomaly']))
    edge_anomaly.appendChild(edge_anomalyContent)
    annotation.appendChild(edge_anomaly)          #edge_anomaly标签结束
    corner_anomaly = xmlBuilder.createElement("corner_anomaly")  # corner_anomaly标签
    corner_anomalyContent = xmlBuilder.createTextNode(str(configInfo['color']['corner_anomaly']))
    corner_anomaly.appendChild(corner_anomalyContent)
    annotation.appendChild(corner_anomaly)          #corner_anomaly标签结束
    white_point_blemishes = xmlBuilder.createElement("white_point_blemishes")  # white_point_blemishes标签
    white_point_blemishesContent = xmlBuilder.createTextNode(str(configInfo['color']['white_point_blemishes']))
    white_point_blemishes.appendChild(white_point_blemishesContent)
    annotation.appendChild(white_point_blemishes)          #white_point_blemishes标签结束
    light_block_blemishes = xmlBuilder.createElement("light_block_blemishes")  # light_block_blemishes标签
    light_block_blemishesContent = xmlBuilder.createTextNode(str(configInfo['color']['light_block_blemishes']))
    light_block_blemishes.appendChild(light_block_blemishesContent)
    annotation.appendChild(light_block_blemishes)          #light_block_blemishes标签结束
    dark_spot_blemishes = xmlBuilder.createElement("dark_spot_blemishes")  # dark_spot_blemishes标签
    dark_spot_blemishesContent = xmlBuilder.createTextNode(str(configInfo['color']['dark_spot_blemishes']))
    dark_spot_blemishes.appendChild(dark_spot_blemishesContent)
    annotation.appendChild(dark_spot_blemishes)          #dark_spot_blemishes标签结束
    aperture_blemishes = xmlBuilder.createElement("aperture_blemishes")  # aperture_blemishes标签
    aperture_blemishesContent = xmlBuilder.createTextNode(str(configInfo['color']['aperture_blemishes']))
    aperture_blemishes.appendChild(aperture_blemishesContent)
    annotation.appendChild(aperture_blemishes)          #aperture_blemishes标签结束
    f = open("config.xml", 'w')
    xmlBuilder.writexml(f, indent='\t', newl='\n', addindent='\t', encoding='utf-8')
    f.close()
    
# 解析配置文件
def readConfig():
    tree = ET.parse('config.xml')
    root = tree.getroot()
    imageShape = tree.find('imageShape')
    configDict = {'color':{}}
    configDict['modelPath']      = root.find('modelPath').text
    configDict['imageShape']     = [int(imageShape.find('width').text), int(imageShape.find('height').text)]
    configDict['confidence']     = float(root.find('confidence').text)
    configDict['nms_iou']        = float(root.find('nms_iou').text)
    configDict['maxBoxes']       = int(root.find('maxBoxes').text)
    configDict['letterboxImage'] = bool(root.find('letterboxImage').text)
    configDict['detectAnsPath']   = root.find('detectAnsPath').text
    configDict['color']['edge_anomaly'] = toTuple(root.find('edge_anomaly').text)
    configDict['color']['corner_anomaly'] = toTuple(root.find('corner_anomaly').text)
    configDict['color']['white_point_blemishes'] = toTuple(root.find('white_point_blemishes').text)
    configDict['color']['light_block_blemishes'] = toTuple(root.find('light_block_blemishes').text)
    configDict['color']['dark_spot_blemishes'] = toTuple(root.find('dark_spot_blemishes').text)
    configDict['color']['aperture_blemishes'] = toTuple(root.find('aperture_blemishes').text)
    configDict['task'] = []
    for task in root.iter('runtask'):
        configDict['task'].append(task)
    for task in root.iter('task'):
        configDict['task'].append(task)
    return configDict

# 加载配置文件
def loadConfig():
    # 默认配置信息
    defaultConfigDict = {
        'modelPath': "model/",
        'imageShape': [832, 608],
        'confidence': 0.5,
        'nms_iou': 0.3,
        'maxBoxes': 100,
        'letterboxImage': False,
        'detectAnsPath': 'detectAns/',
        'color': {
            "edge_anomaly": (238, 238, 0),
            "corner_anomaly": (0, 255, 0),
            "white_point_blemishes": (0, 255, 255),
            "light_block_blemishes": (0, 0, 255),
            "dark_spot_blemishes": (226, 43, 138),
            "aperture_blemishes": (98, 28, 139)},
        'task':[]}
    # 尝试打开配置文件， 如果失败就将默认配置写入配置文件并返回
    try:
        configDict = readConfig()
    except Exception as E:
        print('Error: %s' %(E)) 
        writeConfig(defaultConfigDict)
        return defaultConfigDict
    return configDict

# 修改配置文件
def reviseConfig(key, vaule=None, secondKey=None, reviseType=None):
    tree = ET.parse('config.xml')
    root = tree.getroot()
    if reviseType == 'a':
        taskEle = ET.Element(key)
        taskEle.text = vaule
        root.append(taskEle)
    elif reviseType == 'd':
        for task in root.findall(key):
            root.remove(task)
    elif secondKey is None:
        root.find(key).text = vaule
    elif reviseType is None:
        root.find(key).find(secondKey).text = vaule
    tree.write('config.xml', 'UTF-8')
    
    
        