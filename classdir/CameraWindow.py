import os
from queue import Queue
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QCloseEvent
from classdir.Ui_camera import Ui_MainWindow
from classdir.Worker import *
from classdir.Task import *

class CameraWindow(QMainWindow):
    closeSignal = pyqtSignal()
    fileQueueSignal = pyqtSignal()
    loadHistorySignal = pyqtSignal()
    def __init__(self, yoloConfig, colorDict):
        self.yoloConfig = yoloConfig
        self.colorDict = colorDict
        # 图像队列
        self.fileQueue = Queue()
        # 绘制图像的线程队列
        self.drawHomeQueue = WorkQueue()
        # 检测结果列表
        self.detectInfoList = []
        # 当前已读图像数量
        self.readImageNum = 0
        # 当前瑕疵瓷砖总数
        self.flawNum = 0
        # 当前正常瓷砖总数
        self.noFlawNum = 0
        # 当前显示的瑕疵信息的索引
        self.showCameraIndex = 0
        super(CameraWindow, self).__init__()
        # 界面初始化
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.statusBar().showMessage("正在搜索摄像头")
        self.__ui.enterButton.setEnabled(False)
        # 设置隐藏QTabWidget的标签
        self.__ui.cameraTabWidget.tabBar().hide()
        # 连接信号和槽
        self.__connectSignalAndSlot()
        # 设置鼠标悬停提示信息
        self.__setToolTip()
        # 初始化窗口
        self.__initWindow()
        # 显示窗口
        self.show()
        self.info = [False]   
        # 检测摄像头
        self.getCameraThread = getCameraIndex()
        self.getCameraThread.CameraIndexSignal.connect(self.setCamera)
        self.getCameraThread.start()
    
    # 连接信号和槽
    def __connectSignalAndSlot(self):
        self.__ui.inputImage.wheelEventSignal.connect(self.linkageImage)
        self.__ui.outImage.wheelEventSignal.connect(self.linkageImage)
        self.__ui.inputImage.mouseReleaseSignal.connect(self.mouseReleaseLinkage)
        self.__ui.outImage.mouseReleaseSignal.connect(self.mouseReleaseLinkage)
        self.__ui.inputImage.mousePressSignal.connect(self.mousePressLinkage)
        self.__ui.outImage.mousePressSignal.connect(self.mousePressLinkage)
        self.__ui.inputImage.mouseMoveSignal.connect(self.mouseMoveLinkage)
        self.__ui.outImage.mouseMoveSignal.connect(self.mouseMoveLinkage)
        self.__ui.floderButton.clicked.connect(self.clickFloderButton)
        self.__ui.enterButton.clicked.connect(self.clickEnter)
        self.__ui.cancelButton.clicked.connect(self.close)
        self.fileQueueSignal.connect(self.updateFileList)

    # 重写关闭事件
    def closeEvent(self, a0: QCloseEvent) -> None:
        self.info[0] = False
        self.closeSignal.emit()
        return super().closeEvent(a0)


    # 设置可以摄像头
    def setCamera(self, CameraIndexList):
        if len(CameraIndexList) == 0:
            QMessageBox.critical(self,'Error','设备未连接摄像头!!!',QMessageBox.Ok)
            self.close()
        else:
            self.__ui.comboBox.clear()
            self.__ui.comboBox.addItems(CameraIndexList)
            self.statusBar().showMessage("")
            self.__ui.enterButton.setEnabled(True)
    # 选择文件夹
    def clickFloderButton(self):
        path = QFileDialog.getExistingDirectory(
                 self, "选择模型位置", os.getcwd())
        if path != "":
            self.__ui.floderEdit.setText(path)
            self.statusBar().showMessage("")
            self.__ui.enterButton.setEnabled(True)

    # 点确定按钮
    def clickEnter(self):
        floder_ = self.__ui.floderEdit.text().replace('\\', '/')
        if not os.path.isdir(floder_):
            QMessageBox.critical(self,'Error','请检查图像路径是否正确!!!',QMessageBox.Ok)
            return
        # 状态
        self.info[0] = True
        self.info.append(floder_ if floder_[-1] == '/' else floder_ + '/')
        self.info.append(self.__ui.timeNum.value())
        self.info.append(int(self.__ui.comboBox.currentText()))
        self.__ui.cameraTabWidget.setCurrentIndex(1)
        self.start()
    
    # 初始化窗口
    def __initWindow(self):
        # 设置瑕疵颜色
        (b, g, r) = self.colorDict['edge_anomaly']
        self.__ui.sideColor.setStyleSheet('font: 150 14pt "Agency FB";color:rgb' + str((r, g, b)) + ";")
        (b, g, r) = self.colorDict['corner_anomaly']
        self.__ui.angleColor.setStyleSheet('font: 150 14pt "Agency FB";color:rgb' + str((r, g, b)) + ";")
        (b, g, r) = self.colorDict['white_point_blemishes']
        self.__ui.whiteColor.setStyleSheet('font: 150 14pt "Agency FB";color:rgb' + str((r, g, b)) + ";")
        (b, g, r) = self.colorDict['light_block_blemishes']
        self.__ui.lightColor.setStyleSheet('font: 150 14pt "Agency FB";color:rgb' + str((r, g, b)) + ";")
        (b, g, r) = self.colorDict['dark_spot_blemishes']
        self.__ui.darkColor.setStyleSheet('font: 150 14pt "Agency FB";color:rgb' + str((r, g, b)) + ";")
        (b, g, r) = self.colorDict['aperture_blemishes']    
        self.__ui.apertureColor.setStyleSheet('font: 150 14pt "Agency FB";color:rgb' + str((r, g, b)) + ";")
        # 初始化ImageBox
        self.__ui.inputImage.loadImage(QPixmap('icon/noinfo.png'))
        self.__ui.outImage.loadImage(QPixmap('icon/noinfo.png'))

    # 设置鼠标悬停提示信息
    def __setToolTip(self):
        self.__ui.inputImage.setToolTip("滚轮缩放图像")
        self.__ui.outImage.setToolTip("滚轮缩放图像")

    # 开始检测
    def start(self):
        self.finishNum = 0
        self.isDetect = False
        self.isModel = False
        self.statusBar().showMessage("准备中")
        self.readyYOLOThread = ReadyYOLO(self.yoloConfig)
        self.readyYOLOThread.stateSignal.connect(self.acceptanceModel)
        self.readyYOLOThread.start()

    # 接受模型
    def acceptanceModel(self, msg, model):
        if msg == "OK":
            self.model = model[0]
            self.isModel = True
            self.statusBar().showMessage("检测中")
            self.photographThread = Photograph(self.info)
            self.photographThread.fileNameSignal.connect(self.acceptFileName)
            self.photographThread.start()
        else:
            QMessageBox.critical(self,'Error','出现错误!!!',QMessageBox.Ok)
            self.close()    
            
    # 接受文件名
    def acceptFileName(self, fileName):
        if fileName == "Error":
            QMessageBox.critical(self,'Error','摄像头断开!!!',QMessageBox.Ok)
            self.close()
            return
        self.fileQueue.put(fileName)
        self.fileQueueSignal.emit()
    
    # fileQueueSignal处理
    def updateFileList(self):
        if self.isDetect or self.fileQueue.empty() or not self.isModel:
            return
        self.fileList = []
        while not self.fileQueue.empty():
            self.fileList.append(self.info[1] + self.fileQueue.get())
        self.isDetect = True
        # 创建检测线程
        self.detectThread = DetectThreadCamera(self.model, self.fileList, self.yoloConfig)
        # 绑定线程信号
        self.detectThread.endSignal.connect(self.dealDetectState)
        self.detectThread.setectAns.connect(self.receiveDetectInfo)
        self.detectThread.start()
    
    # 处理检测线程的状态信号
    def dealDetectState(self):
        self.isDetect = False
        self.fileQueueSignal.emit()
        
            
    # 接受传回的检测信息
    def receiveDetectInfo(self, detectInfo):
        self.finishNum += 1
        if (self.finishNum % 10 == 0):
            self.loadHistorySignal.emit()
        self.detectInfoList.append(detectInfo)
        # 统计检测结果
        self.readImageNum += 1
        if detectInfo.isHaveFlaw:
            self.flawNum += 1
        else:
            self.noFlawNum += 1
        self.__ui.currentNum.setText(str(self.readImageNum))
        self.__ui.standNum.setText(str(self.noFlawNum))
        self.__ui.flawNum.setText(str(self.flawNum))
        self.showCamera(self.finishNum - 1)

    # 显示瓷砖
    def showCamera(self, index):
        self.detectInfoList[index].setConfidence(self.yoloConfig['confidence'])
        tmpThread = drawHome(self.detectInfoList[index], self.colorDict)
        tmpThread.endSignal.connect(self.resiveImg)
        self.drawHomeQueue.add(tmpThread)
        self.__ui.nameLabel.setText(self.detectInfoList[index].path.split("/")[-1])
        self.__ui.sideNum.setText(str(self.detectInfoList[index].flawStatistics['edge_anomaly']))
        self.__ui.angleNum.setText(str(self.detectInfoList[index].flawStatistics['corner_anomaly']))
        self.__ui.whiteNum.setText(str(self.detectInfoList[index].flawStatistics['white_point_blemishes']))
        self.__ui.lightNum.setText(str(self.detectInfoList[index].flawStatistics['light_block_blemishes']))
        self.__ui.darkNum.setText(str(self.detectInfoList[index].flawStatistics['dark_spot_blemishes']))
        self.__ui.apertureNum.setText(str(self.detectInfoList[index].flawStatistics['aperture_blemishes']))
    
    # 接受绘制完成的图像
    def resiveImg(self, img, img_):
        self.__ui.outImage.setImage(img)
        self.__ui.inputImage.setImage(img_)
        self.resiveImgThread_ = self.drawHomeQueue.delWork()

    # 切换显示图像
    # def swapShowImage(self, msg=None):
    #     if msg == "inputImage" or self.sender().objectName() == "previouImageButton":
    #         if self.showCameraIndex - 1 < 0:
    #             return
    #         else:
    #             self.showCameraIndex -= 1
    #     elif msg == "outImage" or self.sender().objectName() == "nextImageButton":
    #         if self.showCameraIndex + 1 >= self.readImageNum:
    #             return
    #         else:
    #             self.showCameraIndex += 1
    #     self.showCamera(self.showCameraIndex)
        
    # 实现图像联动
    # 鼠标滚动联动
    def linkageImage(self, name, event):
        self.__ui.outImage.wheelEvents(event) \
        if name == "inputImage" \
        else self.__ui.inputImage.wheelEvents(event) \
        if name == "outImage" else None
    # 鼠标释放联动        
    def mouseReleaseLinkage(self, name, event):
        self.__ui.outImage.mouseReleaseEvents(event) \
        if name == "inputImage" \
        else self.__ui.inputImage.mouseReleaseEvents(event) \
        if name == "outImage" else None
    # 鼠标按下联动
    def mousePressLinkage(self, name, event):
        self.__ui.outImage.mousePressEvents(event) \
        if name == "inputImage" \
        else self.__ui.inputImage.mousePressEvents(event) \
        if name == "outImage" else None
    # 鼠标移动联动
    def mouseMoveLinkage(self, name, event):
        self.__ui.outImage.mouseMoveEvents(event) \
        if name == "inputImage" \
        else self.__ui.inputImage.mouseMoveEvents(event) \
        if name == "outImage" else None
