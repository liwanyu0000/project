from PyQt5.Qt import QThread
from PyQt5.QtCore import pyqtSignal
from utils.utilsXml import reviseConfig
from queue import Queue
import os


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
            
        
    


# 保存配置
class saveConfig(QThread):
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
class searchFile(QThread):
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
