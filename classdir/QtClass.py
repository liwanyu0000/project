
from PyQt5.QtWidgets import QSlider, QLabel, QGraphicsItem, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import pyqtSignal, QSize, Qt
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
    
class ImageBox(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.zoomInTimes = 1
        self.maxZoomInTimes = 30
        # 创建场景
        self.graphicsScene = QGraphicsScene()
        # 以鼠标所在位置为锚点进行缩放
        self.setTransformationAnchor(self.AnchorUnderMouse)
        # 隐藏滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        # 放入空QPixmap
        self.loadImage(QtGui.QPixmap())
    # 滚动鼠标滚轮缩放图片
    def wheelEvent(self, event: QtGui.QWheelEvent) -> None:
        if event.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()  
    # 缩放图片
    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        if self.zoomInTimes > 0:
            return
        # 调整图片大小
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size()*ratio
        if ratio < 1:
            self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)
        else:
            self.resetTransform()
    def loadImage(self, pixmap:QtGui.QPixmap):
        self.pixmap = pixmap
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.displayedImageSize = QSize(0, 0)# 平滑缩放
        self.pixmapItem.setTransformationMode(Qt.SmoothTransformation)
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        # 设置场景
        self.graphicsScene.addItem(self.pixmapItem)
        self.setScene(self.graphicsScene)
    # 重置变换
    def resetTransform(self) -> None:
        super().resetTransform()
        self.zoomInTimes = 0
        self.__setDragEnabled(False)
        return super().resetTransform()
    # 根据图片的尺寸决定是否启动拖拽功能
    def __isEnableDrag(self):
        v = self.verticalScrollBar().maximum() > 0
        h = self.horizontalScrollBar().maximum() > 0
        return v or h
    # 设置拖拽是否启动
    def __setDragEnabled(self, isEnabled: bool):
        self.setDragMode(self.ScrollHandDrag if isEnabled else self.NoDrag)
    # 获取显示的图像和原始图像的缩放比例
    def __getScaleRatio(self):
        if self.pixmap.isNull():
            return 1
        pw = self.pixmap.width()
        ph = self.pixmap.height()
        rw = min(1, self.width()/pw)
        rh = min(1, self.height()/ph)
        return min(rw, rh)
 
    def fitInView(self, item: QGraphicsItem, mode=Qt.KeepAspectRatio):
        """ 缩放场景使其适应窗口大小 """
        super().fitInView(item, mode)
        self.displayedImageSize = self.__getScaleRatio()*self.pixmap.size()
        self.zoomInTimes = 0
    # 放大图像
    def zoomIn(self, viewAnchor=QGraphicsView.AnchorUnderMouse):
        if self.zoomInTimes == self.maxZoomInTimes:
            return
        self.setTransformationAnchor(viewAnchor)
        self.zoomInTimes += 1
        self.scale(1.1, 1.1)
        self.__setDragEnabled(self.__isEnableDrag())
        # 还原 anchor
        self.setTransformationAnchor(self.AnchorUnderMouse)
    # 缩小图像
    def zoomOut(self, viewAnchor=QGraphicsView.AnchorUnderMouse):
        if self.zoomInTimes == 0 and not self.__isEnableDrag():
            return
        self.setTransformationAnchor(viewAnchor)
        self.zoomInTimes -= 1
        # 原始图像的大小
        pw = self.pixmap.width()
        ph = self.pixmap.height()
        # 实际显示的图像宽度
        w = self.displayedImageSize.width()*1.1**self.zoomInTimes
        h = self.displayedImageSize.height()*1.1**self.zoomInTimes
        if pw > self.width() or ph > self.height():
            # 在窗口尺寸小于原始图像时禁止继续缩小图像比窗口还小
            if w <= self.width() and h <= self.height():
                self.fitInView(self.pixmapItem)
            else:
                self.scale(1/1.1, 1/1.1)
        else:
            # 在窗口尺寸大于图像时不允许缩小的比原始图像小
            if w <= pw:
                self.resetTransform()
            else:
                self.scale(1/1.1, 1/1.1)
        self.__setDragEnabled(self.__isEnableDrag())
        # 还原 anchor
        self.setTransformationAnchor(self.AnchorUnderMouse)
    