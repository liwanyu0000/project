import time

# 存储检测结果
class DetectInfo(object):
    # flaw : [x1, y1, x2, y2, score, class]
    def __init__(self, 
                 imagePath,     # 图像存储路径
                 imageWidth,    # 图像宽
                 imageHeight,   # 图像高
                 depth) -> None:# 图像通道数
        self.path = imagePath
        self.width = imageWidth
        self.height = imageHeight
        self.depth = depth
        self.detectTime = None
        self.detectTimes = None
        self.flawList = []
        self.showFlawList = []
        self.flawStatistics = {
            "edge_anomaly" : 0,
            "corner_anomaly" : 0,
            "white_point_blemishes" : 0,
            "light_block_blemishes" : 0,
            "dark_spot_blemishes" : 0,
            "aperture_blemishes" : 0,
            "all" : 0}
    # 添加瑕疵
    def addFlaw(self, flaw):
        self.flawList.append(flaw)
    # 设置检测时间
    def updateTime(self, detectTime):
        self.detectTime = detectTime
        self.detectTimes = time.strptime(self.detectTime, "%Y-%m-%d %H:%M:%S")
        self.detectTimes = time.mktime(self.detectTimes)
    # 设置置信度
    def setConfidence(self, confidence):
        self.showFlawList = []
        self.flawStatistics = {
            "edge_anomaly" : 0,
            "corner_anomaly" : 0,
            "white_point_blemishes" : 0,
            "light_block_blemishes" : 0,
            "dark_spot_blemishes" : 0,
            "aperture_blemishes" : 0,
            "all" : 0}
        for flaw in self.flawList:
            if flaw[4] >= confidence:
                self.showFlawList.append(flaw)
                self.flawStatistics['all'] += 1
                self.flawStatistics[flaw[5]] += 1
        if self.flawStatistics['all'] == 0:
            self.isHaveFlaw = False
        else:
            self.isHaveFlaw = True
        