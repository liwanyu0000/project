from PyQt5.QtWidgets import QSlider, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui

class MySlider(QSlider):
    def __init__(self, parent=None):
        super(QSlider, self).__init__(parent)
    
    # 重载鼠标点击事件
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        pos = ev.pos().x() / self.width()
        self.setValue(round(pos * (self.maximum() - self.minimum()) + self.minimum()))
        return super().mousePressEvent(ev)
        
class MyLabel(QLabel):
    clickSignal = pyqtSignal(str)
    doubleClickSignal = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(QLabel, self).__init__(parent)
    
    # 重载鼠标双击事件
    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.doubleClickSignal.emit(self.objectName())
        return super().mouseDoubleClickEvent(a0)
    
    # 重载鼠标点击事件
    def mousePressEvent(self, ev: QtGui.QMouseEvent) -> None:
        self.clickSignal.emit(self.objectName())
        return super().mousePressEvent(ev)
        
    