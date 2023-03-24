
# 存储检测结果
class DetectInfo(object):
    # flaw : [x1, y1, x2, y2, score, class]
    flawList = []
    detectTime = None
    def __init__(self, 
                 imagePath,     # 图像存储路径
                 imageName,     # 图像名字
                 imageWidth,    # 图像宽
                 imageHeight,   # 图像高
                 depth) -> None:# 图像通道数
        self.path = imagePath
        self.name = imageName
        self.width = imageWidth
        self.height = imageHeight
        self.depth = depth
    # 添加瑕疵
    def addFlaw(self, flaw):
        self.flawList.append(flaw)
    # 设置检测时间
    def updateTime(self, detectTime):
        self.detectTime = detectTime
