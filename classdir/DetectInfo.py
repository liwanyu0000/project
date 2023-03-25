from PyQt5.QtGui import QImage, QPixmap
import cv2

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
        if len(self.showFlawList) == 0:
            self.isHaveFlaw = False
        else:
            self.isHaveFlaw = True
    # 绘图            
    def draw(self, colordist):
        img = cv2.imread(self.path)
        for flaw in self.showFlawList:
            img = cv2.rectangle(img, (flaw[0], flaw[1]), (flaw[2], flaw[3]), colordist[flaw[5]], 2)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = QImage(img.data, self.width, self.height, 
                     self.width * self.depth, QImage.Format_RGB888)
        return QPixmap(img)