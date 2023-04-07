import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from utils.utilsXml import loadConfig
from classdir.Ui_Window import Ui_MainWindow
from classdir.CameraWindow import CameraWindow
from classdir.Worker import *
from classdir.Dialog import *
from classdir.Task import *

class MainWindow(QMainWindow):
    # 支持的图像格式列表
    includedExtensions = ['jpg', 'jpeg', 'bmp', 'png', 'dib', 'jpe', 'pbm', 'pgm', 'ppm', 'tiff', 'tif']
    # 修改配置文件的线程队列
    resiveConfigQueue = WorkQueue()
    # 修改检测结果置信度的线程队列
    resiveAnsQueue = WorkQueue()
    # 加载主页图像的线程队列
    loadHomeImageQueue = WorkQueue()
    # 加载历史检测结果的线程队列
    loadHistoryQueue = WorkQueue()
    # 绘制主页图像的线程队列
    drawHomeQueue = WorkQueue()
    # 任务列表
    taskList = []
    # 检测结果列表
    detectInfoList = []
    # 历史检测结果列表
    historyDetectInfoList = []
    # 定义信号
    # 任务列表改动时发送信号
    changeTaskListSignal = pyqtSignal()
    # 置信度改变时发送信号
    changeConfidenceSignal = pyqtSignal()
    # 正在执行的任务索引(无任务时为-1)
    runindex = -1
    # 当前已读图像数量
    readImageNum = 0
    # 当前瑕疵瓷砖总数
    flawNum = 0
    # 当前正常瓷砖总数
    noFlawNum = 0
    # 正在显示的任务文件列表(当显示正在执行的任务文件列表时，可以实时刷新)
    showFileIndex = -1
    # 当前显示的瑕疵信息的索引
    showHomeIndex = 0
    # 当前任务是否暂停
    __isStop = False
    def __init__(self):
        super(MainWindow, self).__init__()
        # 界面初始化
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        # 设置隐藏QTabWidget的标签
        self.__ui.rightTabWidget.tabBar().hide()
        # 初始化TableWidget
        self.__initTableWidget()
        # 连接信号和槽
        self.__connectSignalAndSlot()
        # 设置状态栏
        self.__initStaturBar()
        # 设置鼠标悬停提示信息
        self.__setToolTip()
        # 初始化窗口
        self.__initWindow()
        # 加载历史检测结果
        self.loadHistory()
    
    # 连接信号和槽
    def __connectSignalAndSlot(self):
        self.__ui.toHomeButton.clicked.connect(self.swapInterface)
        self.__ui.toQueryButton.clicked.connect(self.swapInterface)
        self.__ui.toShowTaskButton.clicked.connect(self.swapInterface)
        self.__ui.confidenceNum.valueChanged.connect(self.changeConfidenceSlider)
        self.__ui.confidenceSlider.valueChanged.connect(self.changeConfidenceSpinbox)
        self.__ui.widthNum.valueChanged.connect(self.changeWidth)
        self.__ui.heightNum.valueChanged.connect(self.changeHeight)
        self.__ui.sideColor.clickSignal.connect(self.changeColor)
        self.__ui.angleColor.clickSignal.connect(self.changeColor)
        self.__ui.darkColor.clickSignal.connect(self.changeColor)
        self.__ui.lightColor.clickSignal.connect(self.changeColor)
        self.__ui.apertureColor.clickSignal.connect(self.changeColor)
        self.__ui.whiteColor.clickSignal.connect(self.changeColor)
        self.__ui.settingButton.clicked.connect(self.clickSettingButton)
        self.__ui.fileButton.clicked.connect(self.clickfileButton)
        self.__ui.folderButton.clicked.connect(self.clickfolderButton)
        self.__ui.cameraButton.clicked.connect(self.clickcameraButton)
        self.__ui.expandButton.clicked.connect(self.clickExpandButton)
        self.__ui.putAwayButton.clicked.connect(self.clickPutAwayButton)
        self.changeTaskListSignal.connect(self.responseChangeTaskList)
        self.__ui.taskQenueTableList.cellDoubleClicked.connect(self.delTask)
        self.__ui.taskQenueTableList.cellClicked.connect(self.showFileList)
        self.__ui.runTaskInfoLabel.clickSignal.connect(self.runingFileList)
        self.__ui.fileExpandButton.clicked.connect(self.clickFileExpandButton)
        self.__ui.fileListTableList.cellDoubleClicked.connect(self.fileListShowImage)
        self.__ui.enterButton.clicked.connect(self.clickEnterButton)
        self.__ui.stopButton.clicked.connect(self.clickStopButton)
        self.__ui.inputImage.doubleClickSignal.connect(self.swapShowImage)
        self.__ui.outImage.doubleClickSignal.connect(self.swapShowImage)
        self.changeConfidenceSignal.connect(self.resiveAns)
        self.__ui.inputImage.wheelEventSignal.connect(self.linkageImage)
        self.__ui.outImage.wheelEventSignal.connect(self.linkageImage)
        self.__ui.inputImage.mouseReleaseSignal.connect(self.mouseReleaseLinkage)
        self.__ui.outImage.mouseReleaseSignal.connect(self.mouseReleaseLinkage)
        self.__ui.inputImage.mousePressSignal.connect(self.mousePressLinkage)
        self.__ui.outImage.mousePressSignal.connect(self.mousePressLinkage)
        self.__ui.inputImage.mouseMoveSignal.connect(self.mouseMoveLinkage)
        self.__ui.outImage.mouseMoveSignal.connect(self.mouseMoveLinkage)
        self.__ui.previouImageButton.clicked.connect(self.swapShowImage)
        self.__ui.nextImageButton.clicked.connect(self.swapShowImage)
        self.__ui.putAwayFileListButton.clicked.connect(self.clickPutAwayFileListButton)
        self.__ui.expandFileListButton.clicked.connect(self.clickExpandFileListButton)
        self.__ui.tableWidget.cellDoubleClicked.connect(self.swapShowImageFileList)
        self.__ui.queryButton.clicked.connect(self.clickQueryButton)
        self.__ui.queryTableList.cellDoubleClicked.connect(self.showHistoryImage)

    # 初始化窗口
    def __initWindow(self):
        # self.__ui.cameraButton.hide()
        # 加载配置文件
        config = loadConfig()
        # 删除配置文件中的runtask
        self.resiveConfigFile('runtask', reviseType='d')
        # 创建存储yolo配置的字典
        self.yoloConfig = {}
        # yolo输入图像尺寸
        self.yoloConfig['imageShape'] = config['imageShape']
        # yolo模型目录
        self.modelPath = config['modelPath']
        # 置信度
        self.yoloConfig['confidence'] = config['confidence']
        # 识别结果存放目录(如果没有该目录就创建)
        self.yoloConfig['detectAnsPath'] = config['detectAnsPath']
        if not os.path.isdir(self.yoloConfig['detectAnsPath']):
            os.mkdir(self.yoloConfig['detectAnsPath'])    
        # 非极大抑制所用到的nms_iou大小
        self.yoloConfig['nms_iou'] = config['nms_iou']       
        # 设置最大框的数量
        self.yoloConfig['maxBoxes'] = config['maxBoxes']      
        # 该变量用于控制是否使用letterbox_image对输入图像进行不失真的resize
        self.yoloConfig['letterboxImage'] = config['letterboxImage']
        # 瑕疵颜色字典
        self.colorDict = config['color']
        # 加载所有模型文件
        self.loadModelFile()
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
        # 纠正界面上输入图像的宽和高,置信度
        self.__ui.widthNum.setValue(self.yoloConfig['imageShape'][0])
        self.__ui.heightNum.setValue(self.yoloConfig['imageShape'][1])
        self.__ui.confidenceNum.setValue(self.yoloConfig['confidence']) 
        # 初始化按钮
        self.__ui.toHomeButton.hide()
        self.__ui.stopButton.hide()
        self.__ui.expandButton.hide()
        self.__ui.toShowTaskButton.hide()
        self.__ui.enterButton.setText("请添加任务")
        self.__ui.enterButton.setEnabled(False)
        # 加载任务
        for task in config['task']:
            id = len(self.taskList)
            self.taskList.append(LoadTask(id, task.text).load())
            if hasattr(self.taskList[id], 'thread'):
                self.taskList[id].thread.startSignal.connect(self.showMassage)
                self.taskList[id].thread.fileListSignal.connect(self.searchFinish)
                self.taskList[id].thread.start()
        if len(config['task']) != 0:
            self.changeTaskListSignal.emit()
        # 初始化ImageBox
        self.__ui.inputImage.loadImage(QPixmap('icon/noinfo.png'))
        self.__ui.outImage.loadImage(QPixmap('icon/noinfo.png'))
    
    # 初始化状态栏
    def __initStaturBar(self):
        # 修改配置文件提示
        self.resiveConfigFileLabel = QLabel(self)
        self.resiveConfigFileLabel.setStyleSheet("color:rgb(103, 103, 103)")
        self.resiveConfigFileLabel.setText("正在修改配置文件")
        # 搜索文件提示
        self.SearchFileLabel = QLabel(self)
        self.SearchFileLabel.setStyleSheet("color:rgb(103, 103, 103)")
        self.SearchFileLabel.setText("正在搜索文件")
        # 加载历史记录提示
        self.loadHistoryLabel = QLabel(self)
        self.loadHistoryLabel.setStyleSheet("color:rgb(103, 103, 103)")
        self.loadHistoryLabel.setText("正在搜索文件")
        # 检测提示
        self.detectStateLabel  = QLabel(self)
        self.detectStateLabel.setStyleSheet("color:rgb(103, 103, 103)")
        self.detectStateLabel.setText("空闲")
        self.detectStateProgressBar = QProgressBar(self, textVisible=True)
        self.detectStateProgressBar.setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 5px; color: rgb(0, 0, 0);  \
                                        background-color: #FFFFFF; text-align: center;} \
                                        QProgressBar::chunk {background-color: rgb(103, 103, 103); \
                                        border-radius: 10px; margin: 0.1px;  width: 1px;}")
        self.detectStateProgressBar.setValue(20)
        self.statusBar().addPermanentWidget(self.resiveConfigFileLabel)
        self.statusBar().addPermanentWidget(self.SearchFileLabel)
        self.statusBar().addPermanentWidget(self.loadHistoryLabel)
        self.statusBar().addPermanentWidget(self.detectStateLabel)
        self.statusBar().addPermanentWidget(self.detectStateProgressBar)
        self.resiveConfigFileLabel.hide()
        self.SearchFileLabel.hide()
        self.detectStateProgressBar.hide()
        self.loadHistoryLabel.hide()

    # 初始化TableWidget
    def __initTableWidget(self):
        # 设置表格不可更改
        self.__ui.queryTableList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__ui.taskQenueTableList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__ui.fileListTableList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置表格行数(0行)
        self.__ui.queryTableList.setRowCount(0)
        self.__ui.taskQenueTableList.setRowCount(0)
        self.__ui.fileListTableList.setRowCount(0)
        # 设置结果查询整行选择
        self.__ui.queryTableList.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置结果查询显示行、列标题
        self.__ui.queryTableList.horizontalHeader().setVisible(True)
        self.__ui.queryTableList.verticalHeader().setVisible(True)
        self.__ui.taskQenueTableList.horizontalHeader().setVisible(False)
        self.__ui.taskQenueTableList.verticalHeader().setVisible(True)
        self.__ui.fileListTableList.horizontalHeader().setVisible(False)
        self.__ui.fileListTableList.verticalHeader().setVisible(True)
        # 隐藏队列的index列
        self.__ui.taskQenueTableList.setColumnHidden(1, True)
        # self.__ui.queryTableList.setColumnHidden(9, True)
        # 设置文件列表隐藏
        self.__ui.fileListTableList.hide()
        self.__ui.fileListLabel.hide()
        self.__ui.fileExpandButton.hide()
        self.__ui.putAwayFileListButton.hide()
        self.__ui.tableWidget.hide()
        # 设置queryTableList自适应列宽
        self.__ui.queryTableList.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.__ui.queryTableList.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.__ui.queryTableList.horizontalHeader().setSectionResizeMode(8, QHeaderView.ResizeToContents)
        # 设置queryTableList的对齐方式
        # self.__ui.queryTableList.
    
    # 设置鼠标悬停提示信息
    def __setToolTip(self):
        self.__ui.darkColor.setToolTip("点击修改颜色")
        self.__ui.sideColor.setToolTip("点击修改颜色")
        self.__ui.angleColor.setToolTip("点击修改颜色")
        self.__ui.lightColor.setToolTip("点击修改颜色")
        self.__ui.whiteColor.setToolTip("点击修改颜色")
        self.__ui.apertureColor.setToolTip("点击修改颜色")
        self.__ui.inputImage.setToolTip("双击上一张图像，滚轮缩放")
        self.__ui.outImage.setToolTip("双击下一张图像，滚轮缩放")
        self.__ui.nextImageButton.setToolTip("下一张图像")
        self.__ui.previouImageButton.setToolTip("上一张图像")
        self.__ui.putAwayFileListButton.setToolTip("隐藏已检测文件列表")
        self.__ui.expandFileListButton.setToolTip("显示已检测文件列表")
        self.__ui.putAwayButton.setToolTip("隐藏选项")
        self.__ui.expandButton.setToolTip("显示选项")
        self.__ui.tableWidget.setToolTip("双击切换至选中图像")
        self.__ui.runTaskInfoLabel.setToolTip("点击显示文件列表")
        self.__ui.taskQenueTableList.setToolTip("点击显示文件列表, 双击删除选中任务")
        self.__ui.fileListTableList.setToolTip("双击显示图像")
    
    
    # 重写关闭时间
    def closeEvent(self, event):        #关闭窗口触发以下事件 
        clossMessageBox = QMessageBox.question(self, '退出', '你有未完成的任务，你确定要退出吗?' 
                                               if self.runindex != -1 else '你确定要退出吗?', 
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if clossMessageBox == QMessageBox.Yes:
            if self.runindex != -1:
                self.resiveConfigFile('runtask', self.taskList[self.runindex].save(), reviseType='a')
            event.accept()      
        else:  
            event.ignore()

    # 修改配置文件
    def resiveConfigFile(self, key, vaule=None, secondKey=None, reviseType=None):
        tmpThread = SaveConfig(key, vaule, secondKey, reviseType)
        tmpThread.startSignal.connect(self.showMassage)
        tmpThread.saveConfigSignal.connect(self.checkResiveConfigQueue)
        self.resiveConfigQueue.add(tmpThread)
        
    # 开始修改配置文件时,显示消息
    def showMassage(self, msg):
        self.resiveConfigFileLabel.show()
        
    # 配置文件修改完成后, 检查resiveConfigQueue
    def checkResiveConfigQueue(self):
        # 防止 Destroyed while thread is still running, 暂存前一个线程
        self.resiveConfigThread_ = self.resiveConfigQueue.delWork()
        self.resiveConfigFileLabel.hide()
    
     # 修改检测结果置信度, 修改当前显示图像
    def resiveAns(self):
        tmpThread = ResiveAns(self.detectInfoList, self.yoloConfig['confidence'])
        tmpThread.startSignal.connect(self.banDetect)
        tmpThread.resiveAnsSignal.connect(self.resiveAnsQueues)
        self.resiveAnsQueue.add(tmpThread)
        if len(self.detectInfoList) != 0:
            self.showHome(self.showHomeIndex)
        
    # 开始修改检测结果置信度时, 禁止检测
    def banDetect(self):
        self.__ui.enterButton.setEnabled(False)
        
    # 检测结果置信度修改完成后, 恢复检测
    def resiveAnsQueues(self, flawNum, noFlawNum):
        # 防止 Destroyed while thread is still running, 暂存前一个线程
        self.resiveAnsThread_ = self.resiveAnsQueue.delWork()
        self.flawNum = int(flawNum)
        self.noFlawNum = int(noFlawNum)
        self.__ui.standNum.setText(noFlawNum)
        self.__ui.flawNum.setText(flawNum)
        if self.__ui.enterButton.text() == "开始检测":
            self.__ui.enterButton.setEnabled(True)

    # 加载模型文件
    def loadModelFile(self):
        self.modelList = [fileName for fileName in os.listdir(self.modelPath)
                          if any(fileName.endswith(extension) for extension in ['h5'])]
        self.__ui.modelComboBox.clear()
        self.__ui.modelComboBox.addItems(self.modelList) 
    
    # 页面切换    
    def swapInterface(self):
        self.sender().hide()
        index = self.__ui.rightTabWidget.currentIndex()
        if index == 0:
            self.__ui.toHomeButton.show()
        elif index == 1:
            self.__ui.toQueryButton.show()
        else:
            self.__ui.toShowTaskButton.show()
        if self.sender().objectName() == "toHomeButton":
            self.__ui.rightTabWidget.setCurrentIndex(0)
        elif self.sender().objectName() == "toQueryButton":    
            self.__ui.rightTabWidget.setCurrentIndex(1)
            self.loadHistory()
        elif self.sender().objectName() == "toShowTaskButton":
            self.__ui.rightTabWidget.setCurrentIndex(2)
    
    # 显示置信度设置
    def showConfidence(self):
        if self.runindex == -1:
            self.__ui.confidenceLabel.show()
            self.__ui.confidenceNum.show()
            self.__ui.confidenceSlider.show()
    
     # 隐藏置信度设置
    def hideConfidence(self):
        self.__ui.confidenceLabel.hide()
        self.__ui.confidenceNum.hide()
        self.__ui.confidenceSlider.hide()
            
    # 置信度设置
    def changeConfidenceSpinbox(self):
        vaule = self.__ui.confidenceSlider.value()
        self.yoloConfig['confidence'] = vaule / 100
        self.__ui.confidenceNum.setValue(self.yoloConfig['confidence'])
        self.resiveConfigFile('confidence', str(vaule / 100))
        self.changeConfidenceSignal.emit()
        self.loadHistory()
    def changeConfidenceSlider(self):
        vaule = self.__ui.confidenceNum.value()
        self.yoloConfig['confidence'] = vaule
        self.__ui.confidenceSlider.setValue(int(self.yoloConfig['confidence'] * 100))
        self.resiveConfigFile('confidence', str(vaule))

    # 宽设置
    def changeWidth(self):
        vaule = self.__ui.widthNum.value()
        if (vaule % 32 != 0):
            vaule = int(vaule / 32 + 0.5) * 32
        self.yoloConfig['imageShape'][0] = vaule
        self.__ui.widthNum.setValue(vaule)
        self.resiveConfigFile('imageShape', str(vaule), 'width')
        
    # 高设置
    def changeHeight(self):
        vaule = self.__ui.heightNum.value()
        if (vaule % 32 != 0):
            vaule = int(vaule / 32 + 0.5) * 32
        self.yoloConfig['imageShape'][1] = vaule
        self.__ui.heightNum.setValue(vaule)
        self.resiveConfigFile('imageShape', str(vaule), 'height')

    # 设置瑕疵标记颜色
    def changeColor(self, msg):
        color = QColorDialog.getColor()
        if color.isValid():
            if msg == 'edge_anomaly':
                label = self.__ui.sideColor
            elif msg == 'aperture_blemishes':
                label = self.__ui.apertureColor
            elif msg == 'dark_spot_blemishes':
                label = self.__ui.darkColor
            elif msg == 'light_block_blemishes':
                label = self.__ui.lightColor
            elif msg == 'white_point_blemishes':
                label = self.__ui.whiteColor
            elif msg == 'corner_anomaly':
                label = self.__ui.angleColor
            self.colorDict[msg] = (color.blue(), color.green(), color.red())
            self.resiveConfigFile(msg, str(self.colorDict[msg]))
            label.setStyleSheet('font: 150 14pt "Agency FB";color:' + color.name() + ";")
            if len(self.detectInfoList) != 0:
                self.showHome(self.showHomeIndex)
    
    # 点击setting按钮, 打开设置子窗口
    def clickSettingButton(self):
        self.settingDialog = SettingDialog(self.modelPath, self.yoloConfig['detectAnsPath'],
                                     self.yoloConfig['nms_iou'], self.yoloConfig['maxBoxes'], 
                                     self.yoloConfig['letterboxImage'])
        # 如果点击确定, 修改相关参数和配置文件
        if self.settingDialog.exec() == QDialog.Accepted:
            # 修改模型路径，并加载该路径下的模型
            modelPath = self.settingDialog.ui.modelPathEdit.text()
            self.modelPath = modelPath if modelPath[-1] == '/' else modelPath + '/'
            self.resiveConfigFile('modelPath', self.modelPath)
            self.loadModelFile()
            # 修改检测结果存放位置
            detectAnsPath = self.settingDialog.ui.detecAnsPathEdit.text()
            self.yoloConfig['detectAnsPath'] = detectAnsPath if detectAnsPath[-1] == '/' else detectAnsPath + '/'
            self.resiveConfigFile('detectAnsPath', self.yoloConfig['detectAnsPath'])
            self.loadHistory()
            # 修改nms_iou
            self.yoloConfig['nms_iou'] = self.settingDialog.ui.nms_iouNum.value()
            self.resiveConfigFile('nms_iou', str(self.yoloConfig['nms_iou']))
            # 修改最大框的数量
            self.yoloConfig['maxBoxes'] = self.settingDialog.ui.maxBoxesNum.value()
            self.resiveConfigFile('maxBoxes', str(self.yoloConfig['maxBoxes']))
            # 修改letterboxImage
            self.yoloConfig['letterboxImage'] = self.settingDialog.ui.letterboxImageCheckBox.isChecked()
            self.resiveConfigFile('letterboxImage', str(self.yoloConfig['letterboxImage']))
        
    # 点击fileButton按钮选择识别文件
    def clickfileButton(self):
        imageFileList, ok= QFileDialog.getOpenFileNames(self,'选择图像', os.getcwd(),'Image files ' + 
            str(tuple([('*.' + extensions) for extensions in self.includedExtensions])).replace("'", "").replace(",", ""))
        if (ok):
            id = len(self.taskList)
            self.taskList.append(FilesTask(id, imageFileList))
            self.changeTaskListSignal.emit()

    # 点击folderButton按钮选择识别文件夹
    def clickfolderButton(self):
        imageFolderPath = QFileDialog.getExistingDirectory(
                self, "选择文件夹", os.getcwd()) + "/"
        if (imageFolderPath != '/'):
            id = len(self.taskList)
            self.SearchFileLabel.show()
            self.taskList.append(FolderTask(id, imageFolderPath))
            self.taskList[id].thread.startSignal.connect(self.showMassage)
            self.taskList[id].thread.fileListSignal.connect(self.searchFinish)
            self.taskList[id].thread.start()
            
    # 文件搜索完成后完成文件列表的构建
    def searchFinish(self, fileList, id):
        self.taskList[id].finishBuild(fileList)
        self.changeTaskListSignal.emit()
        self.SearchFileLabel.hide()
        # self.statusBar().showMessage("就绪！")
    
    # 点击cameraButton按钮,选择摄像设备
    def clickcameraButton(self):
        self.yoloConfig['modelFilePath'] = self.modelPath + self.__ui.modelComboBox.currentText()
        self.__ui.cameraButton.setEnabled(False)
        self.cameraWindow = CameraWindow(self.yoloConfig, self.colorDict)
        self.cameraWindow.closeSignal.connect(self.recoverCameraButton) 
        self.cameraWindow.loadHistorySignal.connect(self.loadHistory)
    
    # 恢复cameraButton    
    def recoverCameraButton(self):
        self.__ui.cameraButton.setEnabled(True)

    # 点击putAwayButton按钮隐藏右侧选项
    def clickPutAwayButton(self):
        self.__ui.leftGroupBox.hide()
        self.__ui.expandButton.show()
    # 点击expandButton按钮显示右侧选项
    def clickExpandButton(self):
        self.__ui.leftGroupBox.show()
        self.__ui.expandButton.hide()
    
    # 点击PutAwayFileListButton按钮隐藏文件列表
    def clickPutAwayFileListButton(self):
        self.__ui.tableWidget.hide()
        self.__ui.putAwayFileListButton.hide()
        self.__ui.expandFileListButton.show()
    # 点击ExpandFileListButton按钮显示文件列表
    def clickExpandFileListButton(self):
        self.__ui.tableWidget.show()
        self.__ui.putAwayFileListButton.show()
        self.__ui.expandFileListButton.hide()
    
    # 响应taskList变化
    # taskList变化时重新加载taskQenueTableList
    def responseChangeTaskList(self):
        self.resiveConfigFile('task', reviseType='d')
        row = []
        for (step, task) in enumerate(self.taskList):
            if task.isValid and not task.isStart:
                row.append(step)
        countRow = len(row)
        if countRow == 0 and self.__ui.runTaskInfoLabel.text() == "":
            self.__ui.toShowTaskButton.hide()
            self.__ui.enterButton.setText("请添加任务")
            self.__ui.enterButton.setEnabled(False)
            if (self.__ui.rightTabWidget.currentIndex() == 2):
                self.__ui.rightTabWidget.setCurrentIndex(0)
                self.showConfidence()
                self.__ui.toHomeButton.hide()
        else:
            # 设置taskQenueTableList行数
            self.__ui.taskQenueTableList.setRowCount(countRow)
            for (step, index) in enumerate(row):
                self.resiveConfigFile('task', self.taskList[index].save(), reviseType='a')
                self.__ui.taskQenueTableList.setItem(step, 0, QTableWidgetItem(self.taskList[index].name))
                self.__ui.taskQenueTableList.setItem(step, 1, QTableWidgetItem(str(index)))
            if (self.__ui.rightTabWidget.currentIndex() != 2):
                self.__ui.toShowTaskButton.show()
            if (self.__ui.enterButton.text() == "请添加任务"):
                self.__ui.enterButton.setText("开始检测")
                self.__ui.enterButton.setEnabled(True)
    
    # 双击删除任务
    def delTask(self, row):
        reply = QMessageBox.question(self, '删除任务', '确定要删除该任务？',
                             QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        
        if (reply == QMessageBox.Yes):
            self.taskList[int(self.__ui.taskQenueTableList.item(row, 1).text())].delTask()
            self.changeTaskListSignal.emit()
            self.clickFileExpandButton()
    
    # 点击显示文件列表
    def showFileList(self, row):
        self.showFileIndex = int(self.__ui.taskQenueTableList.item(row, 1).text())
        fileList = self.taskList[self.showFileIndex].fileList
        countRow = len(fileList)
        self.__ui.fileListTableList.setRowCount(countRow)
        for (step, fileName) in enumerate(fileList):
                self.__ui.fileListTableList.setItem(step, 0, QTableWidgetItem(fileName))
        self.__ui.fileExpandButton.show()
        self.__ui.fileListLabel.show()
        self.__ui.fileListTableList.show()
    
    # 点击显示正在运行任务文件列表
    def runingFileList(self):
        if self.runindex == -1:
            return
        self.showFileIndex = self.runindex
        fileList = self.taskList[self.runindex].fileList
        countRow = len(fileList)
        self.__ui.fileListTableList.setRowCount(countRow)
        for (step, fileName) in enumerate(fileList):
                self.__ui.fileListTableList.setItem(step, 0, QTableWidgetItem(fileName))
        self.__ui.fileExpandButton.show()
        self.__ui.fileListLabel.show()
        self.__ui.fileListTableList.show()
        
    
    # 点击FileExpandButton按钮,隐藏文件列表
    def clickFileExpandButton(self):
        self.__ui.fileExpandButton.hide()
        self.__ui.fileListLabel.hide()
        self.__ui.fileListTableList.hide()
    
    # 双击显示图像
    def fileListShowImage(self, row):
        self.showImageDialog = ShowImageDialog(self.__ui.fileListTableList, row)
        # self.showImageDialog.exec()
    
    # 双击切换主页图像
    def swapShowImageFileList(self, row):
        self.showHomeIndex = row
        self.showHome(row)
        
    # 点击enterButton时, 如果当前无识别任务，则开始识别, 否则取消当前任务
    def clickEnterButton(self):
        if self.__ui.enterButton.text() == '开始检测':
            self.hideConfidence()
            # 获取taskQenueTableList中第一项在taskList中的索引
            self.runindex = int(self.__ui.taskQenueTableList.item(0, 1).text())
            # 获取当前选中的模型文件
            self.yoloConfig['modelFilePath'] = self.modelPath + self.__ui.modelComboBox.currentText()
            # 开始检测
            self.filesNum = self.taskList[self.runindex].start(self.yoloConfig)
            self.finishNum = 0
            # 设置状态栏
            self.detectStateProgressBar.setRange(0, self.filesNum)
            self.detectStateProgressBar.setValue(self.finishNum)
            self.detectStateProgressBar.reset()
            # 绑定线程信号
            self.taskList[self.runindex].detectThread.stateSignal.connect(self.dealDetectState)
            self.taskList[self.runindex].detectThread.setectAns.connect(self.receiveDetectInfo)
            self.taskList[self.runindex].detectThread.start()
            # 改变按钮状态
            self.__ui.enterButton.setText("取消当前任务")
            self.__ui.stopButton.show()
            # 设置当前正在执行的任务
            self.__ui.runTaskInfoLabel.setText(self.__ui.taskQenueTableList.item(0, 0).text())
            # 把当前任务从taskQenueTableList中删除（发送信号即可）
            self.changeTaskListSignal.emit()
        elif self.__ui.enterButton.text() == '取消当前任务':
            self.__ui.enterButton.setEnabled(False)
            self.__ui.stopButton.setEnabled(False)
            self.taskList[self.runindex].stop()
            # 提示是否停止该任务
            clossMessageBox = QMessageBox.question(self, '确认', '你确定要删除该任务?', 
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if clossMessageBox == QMessageBox.Yes:
                self.taskList[self.runindex].delTask()
                self.detectStateLabel.setText("取消中")
            else:
                if not self.__isStop:
                    self.taskList[self.runindex].continues()
                self.__ui.enterButton.setEnabled(True)
                self.__ui.stopButton.setEnabled(True)
    
    # 点击stopButton时, 暂停或开始任务
    def clickStopButton(self):
        if self.__ui.stopButton.text() == "暂停":
            self.__isStop = True
            self.detectStateLabel.setText("暂停中")
            self.__ui.enterButton.setEnabled(False)
            self.__ui.stopButton.setEnabled(False)
            self.taskList[self.runindex].stop()
            self.__ui.stopButton.setText("继续")
        else:
            self.__isStop = False
            self.taskList[self.runindex].continues()
            self.__ui.stopButton.setText("暂停")
    
    # 处理检测线程的状态信号
    def dealDetectState(self, msg):
        self.statusBar().showMessage(msg)
        self.detectStateLabel.setText(msg)
        if (msg == "准备中"):
            self.__ui.enterButton.setEnabled(False)
            self.__ui.stopButton.setEnabled(False)
        elif (msg == "检测中"):
            self.__ui.enterButton.setEnabled(True)
            self.__ui.stopButton.setEnabled(True)
        elif (msg == "检测完成") or (msg == "用户取消"):
            self.loadHistory()
            self.detectStateLabel.setText("空闲")
            self.detectStateProgressBar.hide()
            self.__ui.enterButton.setEnabled(True)
            self.__ui.stopButton.setEnabled(True)
            # 从任务列表中删除该任务
            self.taskList[self.runindex].delTask()
            # 将runTaskInfoLabel的内容置空
            self.__ui.runTaskInfoLabel.setText("")
            # 设置runindex为-1
            self.runindex = -1
            self.showConfidence()
            # 隐藏stopButton按钮
            self.__ui.stopButton.hide()
            # 检查taskQenueTableList中是否还有任务
            if self.__ui.taskQenueTableList.rowCount() == 0:
                self.__ui.toShowTaskButton.hide()
                self.__ui.enterButton.setText("请添加任务")
                self.__ui.enterButton.setEnabled(False)
                if (self.__ui.rightTabWidget.currentIndex() == 2):
                    self.__ui.rightTabWidget.setCurrentIndex(0)
                    self.showConfidence()
                    self.__ui.toHomeButton.hide()
            else:   
                self.__ui.enterButton.setText("开始检测")
            if (msg == "检测完成"):
                # 模拟点击enterButton, 以执行下一个任务
                self.clickEnterButton()
        elif msg == "任务暂停":
            self.__ui.enterButton.setEnabled(True)
            self.__ui.stopButton.setEnabled(True)
        else:
            self.detectStateLabel.setText("出现错误")
            self.detectStateProgressBar.hide()
            # 将runTaskInfoLabel的内容置空
            self.__ui.runTaskInfoLabel.setText("")
            # 设置runindex为-1
            self.runindex = -1
            # 更改按钮设置
            self.__ui.enterButton.setText("开始检测")
            self.__ui.enterButton.setEnabled(True)
            self.__ui.stopButton.hide()
            # 发消息
            self.changeTaskListSignal.emit()
            QMessageBox.critical(self,'Error','出现错误!!!\n1.请检测权重文件\n2.权重文件/图像路径中不能出现中文',QMessageBox.Ok)
        
    # 接受传回的检测信息
    def receiveDetectInfo(self, detectInfo):
        self.finishNum += 1
        if self.finishNum % 10 == 0:
            self.loadHistory()
        if self.finishNum == 1:
            self.detectStateProgressBar.show()
        self.detectStateProgressBar.setValue(self.finishNum)
        self.detectInfoList.append(detectInfo)
        # 如果正在查看任务文件列表, 刷新
        if self.runindex == self.showFileIndex and not self.__ui.fileListTableList.isHidden():
            self.runingFileList()
        # 统计检测结果
        self.readImageNum += 1
        if detectInfo.isHaveFlaw:
            self.flawNum += 1
        else:
            self.noFlawNum += 1
        self.__ui.currentNum.setText(str(self.readImageNum))
        self.__ui.standNum.setText(str(self.noFlawNum))
        self.__ui.flawNum.setText(str(self.flawNum))
        # 更新tableWidget
        self.__ui.tableWidget.setRowCount(self.readImageNum)
        # print(detectInfo.path)
        self.__ui.tableWidget.setItem(self.readImageNum - 1, 0, QTableWidgetItem(detectInfo.path.split("/")[-1]))
        if (self.readImageNum == 1):
            self.showHome(self.showHomeIndex)
    
    # 主页显示瓷砖
    def showHome(self, index):
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
        

    # 鼠标双击切换显示图像
    def swapShowImage(self, msg=None):
        if msg == "inputImage" or self.sender().objectName() == "previouImageButton":
            if self.showHomeIndex - 1 < 0:
                return
            else:
                self.showHomeIndex -= 1
        elif msg == "outImage" or self.sender().objectName() == "nextImageButton":
            if self.showHomeIndex + 1 >= self.readImageNum:
                return
            else:
                self.showHomeIndex += 1
        self.showHome(self.showHomeIndex)
        
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
    
    # 加载历史检测结果
    def loadHistory(self):
        tmpThread = LoadHistory(self.yoloConfig['detectAnsPath'], self.yoloConfig['confidence'])
        tmpThread.startSignal.connect(self.startLoadHistory)
        tmpThread.endSignal.connect(self.endLoadHistory)
        tmpThread.detectInfoSignal.connect(self.showHistory)
        self.loadHistoryQueue.add(tmpThread)
    # 开始加载历史检测结果
    def startLoadHistory(self):
        self.__ui.queryButton.setEnabled(False)
        self.loadHistoryLabel.show()
    # 将历史检测结果显示在结果查询中
    def showHistory(self, step, info:DetectInfo, count=None):
        self.__ui.queryTableList.setRowCount(step + 1)
        item = QTableWidgetItem(info.path.split("/")[-1])
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.__ui.queryTableList.setItem(step, 0, item)
        item = QTableWidgetItem(str(info.flawStatistics['all']))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.__ui.queryTableList.setItem(step, 1, item)
        item = QTableWidgetItem(str(info.flawStatistics['edge_anomaly']))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.__ui.queryTableList.setItem(step, 2, item)
        item = QTableWidgetItem(str(info.flawStatistics['corner_anomaly']))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.__ui.queryTableList.setItem(step, 3, item)
        item = QTableWidgetItem(str(info.flawStatistics['white_point_blemishes']))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.__ui.queryTableList.setItem(step, 4, item)
        item = QTableWidgetItem(str(info.flawStatistics['light_block_blemishes']))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.__ui.queryTableList.setItem(step, 5, item)
        item = QTableWidgetItem(str(info.flawStatistics['dark_spot_blemishes']))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.__ui.queryTableList.setItem(step, 6, item)
        item = QTableWidgetItem(str(info.flawStatistics['aperture_blemishes']))
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.__ui.queryTableList.setItem(step, 7, item)
        item = QTableWidgetItem(info.detectTime)
        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.__ui.queryTableList.setItem(step, 8, item)
        if not count is None:
            self.__ui.queryTableList.setItem(step, 9, QTableWidgetItem(str(count)))
        else:
            self.__ui.queryTableList.setItem(step, 9, QTableWidgetItem(str(step)))
        
    # 完成加载历史检测结果
    def endLoadHistory(self, historyList):
        self.loadHistoryLabel.hide()
        self.__ui.queryButton.setEnabled(True)
        self.loadHistoryThread_ = self.loadHistoryQueue.delWork()
        self.historyDetectInfoList = historyList
    # 点击queryButton    
    def clickQueryButton (self):
        startTime = self.__ui.startTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        endTime = self.__ui.endTime.dateTime().toString("yyyy-MM-dd HH:mm:ss")
        self.loadSearchResultThread = LoadSearchResult(startTime, endTime, self.historyDetectInfoList)
        self.loadSearchResultThread.endSignal.connect(self.finishSearch)
        self.loadSearchResultThread.detectInfoSignal.connect(self.showHistory)
        self.__ui.queryButton.setEnabled(False)
        self.loadSearchResultThread.start()
    
    # 查询完成处理
    def finishSearch(self, msg):
        if msg == "Error":
            QMessageBox.critical(self,'Error','请检查输入的日期!!!',QMessageBox.Ok)
        elif msg == "null":
            self.__ui.queryTableList.setRowCount(0)
            QMessageBox.information(self,'note','无检测结果!!!',QMessageBox.Ok)
        self.__ui.queryButton.setEnabled(True)
    
    # 显示历史图像
    def showHistoryImage(self, row):
        self.showAnsImageDialog = ShowAnsImageDialog(self.__ui.queryTableList, row, self.historyDetectInfoList, self.colorDict)
