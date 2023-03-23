from PyQt5.Qt import QThread
from PyQt5.QtCore import pyqtSignal
from utils.utilsXml import reviseConfig
from queue import Queue


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
    saveConfigSignal = pyqtSignal()
    def __init__(self, key, vaule, secondKey=None) -> None:
        super().__init__()
        self.key = key
        self.vaule = vaule
        self.secondKey = secondKey
    
    def run(self):
        # 修改配置文件
        reviseConfig(self.key, self.vaule, self.secondKey)
        # 发送信号
        self.saveConfigSignal.emit()
        