import os
from queue import Queue
from PyQt5.Qt import QThread
from PyQt5.QtCore import pyqtSignal
from utils.utilsXml import reviseConfig
from classdir.DetectInfo import DetectInfo

# 工作队列
class WorkQueue(Queue):
    def __init__(self, maxsize: int = 0) -> None:
        super().__init__(maxsize)
    def add(self, work):
        self.put(work)
        if self.qsize() == 1:
            work.start()
    def delWork(self):
        tmpWork = self.get()
        if not self.empty():
            self.queue[0].start()
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
    
    # 定义信号
    # 状态提示信号
    stateSignal = pyqtSignal(str)
    # 检测结果信号
    setectAns = pyqtSignal(DetectInfo)
    def __init__(self, yoloConfig:dict, fileList) -> None:
        super().__init__()     
        self.yoloConfig = yoloConfig  
    
    def run(self):
        # 发送信号
        self.stateSignal.emit("准备中")
        # 初始化yolo模型
        from classdir.Yolo import YOLO
        self.model = YOLO(self.yoloConfig['imageShape'])
        # 修改参数
        self.model.setYolo(
            nms_iou=self.yoloConfig['nms_iou'],
            maxBoxes=self.yoloConfig['maxBoxes'],
            letterboxImage=self.yoloConfig['letterboxImage'])
        # 确认权重文件的版本(s,x,m,l)
        for version in ['s', 'x', 'm', 'l']:
            
        
        
         

