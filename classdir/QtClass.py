
from PyQt5.QtWidgets import QSlider, QLabel, QGraphicsItem, QGraphicsPixmapItem, QGraphicsScene, QGraphicsView
from PyQt5.QtCore import pyqtSignal, QSize, Qt, QRectF
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
    doubleClickSignal = pyqtSignal(str)
    wheelEventSignal = pyqtSignal(str, QtGui.QWheelEvent)
    mouseReleaseSignal = pyqtSignal(str, QtGui.QMouseEvent)
    mousePressSignal = pyqtSignal(str, QtGui.QMouseEvent)
    mouseMoveSignal = pyqtSignal(str, QtGui.QMouseEvent)
    flag = True
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.zoomInTimes = 1
        self.maxZoomInTimes = 30
        # 创建场景
        self.graphicsScene = QGraphicsScene()
        # 隐藏滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    # 鼠标按下时发送信号
    def mousePressEvent(self, event: QtGui.QMouseEvent, flag=True) -> None:
        if flag:
            self.mousePressSignal.emit(self.objectName(), event)
        return super().mousePressEvent(event)
    # 鼠标按下时联动
    def mousePressEvents(self, event: QtGui.QMouseEvent) -> None:
        self.mousePressEvent(event, False)
    # 鼠标松开时发送信号
    def mouseReleaseEvent(self, event: QtGui.QMouseEvent, flag=True) -> None:
        if flag:
            self.mouseReleaseSignal.emit(self.objectName(), event)
        return super().mouseReleaseEvent(event)
    # 鼠标松开时联动
    def mouseReleaseEvents(self, event: QtGui.QMouseEvent) -> None:
        self.mouseReleaseEvent(event, False)
    # 鼠标移动发送信号
    def mouseMoveEvent(self, event:QtGui.QMouseEvent, flag=True) -> None:
        if flag:
            self.mouseMoveSignal.emit(self.objectName(), event)
        return super().mouseMoveEvent(event)
    # 鼠标移动时联动
    def mouseMoveEvents(self, event:QtGui.QMouseEvent) -> None:
        self.mouseMoveEvent(event, False)
    # 滚动鼠标滚轮缩放图片
    def wheelEvent(self, event: QtGui.QWheelEvent, flag=True) -> None:
        if flag:
            self.wheelEventSignal.emit(self.objectName(), event)
        if event.angleDelta().y() > 0:
            self.zoomIn()
        else:
            self.zoomOut()  
    # 滚动鼠标滚轮联动缩放图片
    def wheelEvents(self, event: QtGui.QWheelEvent) -> None:
        self.wheelEvent(event, False)
    # 双击切换图片
    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        self.doubleClickSignal.emit(self.objectName())
        return super().mouseDoubleClickEvent(event)
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
    # 加载图像
    def loadImage(self, pixmap:QtGui.QPixmap):
        # 载入图像
        self.pixmap = pixmap
        self.pixmapItem = QGraphicsPixmapItem(self.pixmap)
        self.displayedImageSize = QSize(0, 0)# 平滑缩放
        self.pixmapItem.setTransformationMode(Qt.SmoothTransformation)
        self.setRenderHints(QtGui.QPainter.Antialiasing | QtGui.QPainter.SmoothPixmapTransform)
        # 设置场景
        self.graphicsScene.addItem(self.pixmapItem)
        self.setScene(self.graphicsScene)
        # 调整图片大小
        self.setSceneRect(QRectF(self.pixmap.rect()))
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size()*ratio
        self.fitInView(QGraphicsPixmapItem(QtGui.QPixmap(self.pixmap)))
    # 设置显示的图片
    def setImage(self, pixmap:QtGui.QPixmap):
        self.resetTransform()
        # 刷新图片
        self.pixmap = pixmap
        self.pixmapItem.setPixmap(self.pixmap)
        # 调整图片大小
        self.setSceneRect(QRectF(self.pixmap.rect()))
        ratio = self.__getScaleRatio()
        self.displayedImageSize = self.pixmap.size()*ratio
        self.fitInView(self.pixmapItem, Qt.KeepAspectRatio)
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
    # 缩放场景使其适应窗口大小
    def fitInView(self, item: QGraphicsItem, mode=Qt.KeepAspectRatio):
        super().fitInView(item, mode)
        self.displayedImageSize = self.__getScaleRatio()*self.pixmap.size()
        self.zoomInTimes = 0
    # 放大图像
    def zoomIn(self):
        if self.zoomInTimes == self.maxZoomInTimes:
            return
        self.zoomInTimes += 1
        self.scale(1.1, 1.1)
        self.__setDragEnabled(self.__isEnableDrag())
    # 缩小图像
    def zoomOut(self):
        if self.zoomInTimes == 0 and not self.__isEnableDrag():
            return
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