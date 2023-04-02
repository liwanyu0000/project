import os
from queue import Queue
from PyQt5.Qt import QThread
from PyQt5.QtCore import pyqtSignal
from utils.utilsXml import reviseConfig, analyzeXml
from classdir.DetectInfo import DetectInfo
# from classdir.Task import Task

# 工作队列
class WorkQueue():
    def __init__(self) -> None:
        self.startWork = None   # 正在执行的任务
        self.waitWork = None    # 正在等待的任务
    def add(self, work):
        self.waitWork = work
        if self.startWork is None:
            self.startWork = self.waitWork
            self.waitWork = None
            self.startWork.start()
    def delWork(self):
        tmpWork = self.startWork
        if not self.waitWork is None:
            self.startWork = self.waitWork
            self.waitWork = None
            self.startWork.start()
        else:
            self.startWork = None
        return tmpWork

# 保存配置线程
class SaveConfig(QThread):
    startSignal = pyqtSignal(str)
    saveConfigSignal = pyqtSignal()
    def __init__(self, key, vaule=None, secondKey=None, reviseType=None) -> None:
        super().__init__()
        self.key = key
        self.vaule = vaule
        self.secondKey = secondKey
        self.reviseType = reviseType
    
    def run(self):
        # 发送信号
        self.startSignal.emit("正在修改配置文件")
        # 修改配置文件
        reviseConfig(self.key, self.vaule, self.secondKey, self.reviseType)
        # 发送信号
        self.saveConfigSignal.emit()
   
# 搜索文件夹文件线程 
class SearchFile(QThread):
    startSignal = pyqtSignal(str)
    fileListSignal = pyqtSignal(list, int)
    def __init__(self, folder, includedExtensions, id=None) -> None:
        super().__init__()
        self.folder = folder
        self.includedExtensions = includedExtensions
        self.id = id
    def run(self):
        # 发送信号
        self.startSignal.emit("正在获取文件列表")
        # 获取文件列表
        fileList = [self.folder + fileName for fileName in os.listdir(self.folder)
                if any(fileName.endswith(extension) for extension in self.includedExtensions)]
        # 发送信号
        self.fileListSignal.emit(fileList, self.id)
 
 # 检测线程
class DetectThread(QThread):
    # 瑕疵类型字典
    classesDict = {
        0 : 'edge_anomaly',
        1 : 'corner_anomaly',
        2 : 'white_point_blemishes',
        3 : 'light_block_blemishes',
        4 : 'dark_spot_blemishes',
        5 : 'aperture_blemishes',
    }
    # 定义信号
    # 状态提示信号
    stateSignal = pyqtSignal(str)
    # 检测结果信号
    setectAns = pyqtSignal(DetectInfo)
    def __init__(self, yoloConfig:dict, task) -> None:
        super().__init__()     
        self.yoloConfig = yoloConfig  
        self.task = task
    
    def run(self):
        # 发送信号
        self.stateSignal.emit("准备中")
        # 初始化yolo模型
        os.environ["TF_CPP_MIN_LOG_LEVEL"] = "4"
        os.environ["AUTOGRAPH_VERBOSITY"] = "1"
        from classdir.Yolo import YOLO
        from utils.utilsDetect import detectImage
        self.model = YOLO(self.yoloConfig['imageShape'])
        # 修改参数
        self.model.setYolo(
            nms_iou=self.yoloConfig['nms_iou'],
            maxBoxes=self.yoloConfig['maxBoxes'],
            letterboxImage=self.yoloConfig['letterboxImage'])
        #确认权重文件的版本(s,x,m,l)
        flag = True
        for version in ['s', 'l', 'm', 'x']:
            try:
                self.model.setModelPath(self.yoloConfig['modelFilePath'], version)
                detectinfo = detectImage(self.task.fileList[0], self.yoloConfig['imageShape'], 
                            self.model, self.yoloConfig['detectAnsPath'], self.classesDict)
                flag = False
                break
            except Exception as r:
                print('Error %s' %(r))
        if (flag):
            self.stateSignal.emit("请检测权重文件!!")
            return
         # 发送信号
        self.stateSignal.emit("检测中")
        self.task.updateFileList()
        detectinfo.setConfidence(self.yoloConfig['confidence'])
        self.setectAns.emit(detectinfo)
        while len(self.task.fileList) != 0 and self.task.isValid:
            detectinfo = detectImage(self.task.fileList[0], self.yoloConfig['imageShape'], 
                            self.model, self.yoloConfig['detectAnsPath'], self.classesDict)
            self.task.updateFileList()
            detectinfo.setConfidence(self.yoloConfig['confidence'])
            self.setectAns.emit(detectinfo)
            if not self.task.state:
                self.stateSignal.emit("任务暂停")
                while True:
                    if self.task.state:
                        self.stateSignal.emit("检测中")
                        break
                    self.msleep(10)
        # 发送信号
        if len(self.task.fileList) != 0:
            self.stateSignal.emit("用户取消")
        else:
            self.stateSignal.emit("检测完成")
            
class ResiveAns(QThread):
    startSignal = pyqtSignal(str)
    resiveAnsSignal = pyqtSignal(str, str)
    def __init__(self, detectInfoList, confidence) -> None:
        super().__init__()
        self.detectInfoList = detectInfoList
        self.confidence = confidence
        self.flawNum = 0
        self.noFlawNum = 0
    
    def run(self):
        self.startSignal.emit("开始修正结果")
        for info in self.detectInfoList:
            info.setConfidence(self.confidence)
            if info.isHaveFlaw:
                self.flawNum += 1
            else:
                self.noFlawNum += 1
        self.resiveAnsSignal.emit(str(self.flawNum), str(self.noFlawNum))
        
# # 主页加载图像
# class loadHomeImage(QThread):
#     finishSignal = pyqtSignal()
#     def __init__(self, detectInfo:DetectInfo, inputImage, outImage, confidence, colorDict) -> None:
#         super().__init__()
#         self.detectInfo = detectInfo
#         self.inputImage = inputImage
#         self.outImage = outImage
#         self.confidence = confidence
#         self.colorDict = colorDict
#     def run(self):
#         self.detectInfo.setConfidence(self.confidence)
#         self.inputImage.setImage(QPixmap(self.detectInfo.path))
#         self.outImage.setImage(self.detectInfo.draw(self.colorDict))
#         self.finishSignal.emit()
        
# 加载历史记录

class LoadHistory(QThread):
    startSignal = pyqtSignal()
    endSignal = pyqtSignal(list)
    detectInfoSignal = pyqtSignal(int, DetectInfo)
    def __init__(self, historyDir, confidence) -> None:
        self.historyDir = historyDir
        self.historyList = []
        self.confidence = confidence
        super().__init__()

    def run(self):
        # 发送信号
        self.startSignal.emit()
        # 获取文件列表
        fileList = [self.historyDir + fileName for fileName in os.listdir(self.historyDir)
                if any(fileName.endswith(extension) for extension in ['xml'])]
        for step, file in enumerate(fileList):
            try:
                info = analyzeXml(file)
            except Exception as r:
                print('Error %s' %(r))
                continue
            info.setConfidence(self.confidence)
            self.historyList.append(info)
            self.detectInfoSignal.emit(step, info)
        
        self.endSignal.emit(self.historyList)      
        
            
        
        
         

