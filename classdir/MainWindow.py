from PyQt5.QtWidgets import *
#QMainWindow, QColorDialog, QDialog, QFileDialog, QAbstractItemView, QTableWidgetItem, QMessageBox#, QProgressBar
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from classdir.Ui_Window import Ui_MainWindow
from utils.utilsXml import loadConfig
import os
from classdir.Worker import *
from classdir.Dialog import *
from classdir.Task import *
from classdir.DetectInfo import DetectInfo


class MainWindow(QMainWindow):
    # 支持的图像格式列表
    includedExtensions = ['jpg', 'jpeg', 'bmp', 'png', 'dib', 'jpe', 'pbm', 'pgm', 'ppm', 'tiff', 'tif']
    # 修改配置文件的线程队列
    resiveConfigQueue = WorkQueue()
    # 修改检测结果置信度的线程队列
    resiveAnsQueue = WorkQueue()
    # 加载主页图像的线程队列
    loadHomeImageQueue = WorkQueue()
    # 任务列表
    taskList = []
    # 检测结果列表
    detectInfoList = []
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
        self.statusBar().showMessage("就绪！")
        # 初始化窗口
        self.__initWindow()
    
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
        
    # 初始化窗口
    def __initWindow(self):
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
        # 加载任务、
        for task in config['task']:
            id = len(self.taskList)
            self.taskList.append(LoadTask(id, task.text).load())
            if hasattr(self.taskList[id], 'thread'):
                self.taskList[id].thread.startSignal.connect(self.showMassage)
                self.taskList[id].thread.fileListSignal.connect(self.searchFinish)
                self.taskList[id].thread.start()
        if len(config['task']) != 0:
            self.changeTaskListSignal.emit()
            
    # 初始化TableWidget
    def __initTableWidget(self):
        # 设置表格不可更改
        self.__ui.queryTableList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__ui.taskQenueTableList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.__ui.fileListTableList.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
        # 设置文件列表隐藏
        self.__ui.fileListTableList.hide()
        self.__ui.fileListLabel.hide()
        self.__ui.fileExpandButton.hide()
    
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
        pass
        # self.statusBar().showMessage(msg)
        
    # 配置文件修改完成后, 检查resiveConfigQueue
    def checkResiveConfigQueue(self):
        # 防止 Destroyed while thread is still running, 暂存前一个线程
        self.resiveConfigThread_ = self.resiveConfigQueue.delWork()
        # self.statusBar().showMessage("就绪！")
    
     # 修改检测结果置信度, 修改当前显示图像
    def resiveAns(self):
        tmpThread = ResiveAns(self.detectInfoList, self.yoloConfig['confidence'])
        tmpThread.startSignal.connect(self.banDetect)
        tmpThread.resiveAnsSignal.connect(self.resiveAnsQueues)
        self.resiveAnsQueue.add(tmpThread)
        if len(self.detectInfoList) != 0:
            self.showHome(self.showHomeIndex)
        
    # 开始修改检测结果置信度时, 禁止检测
    def banDetect(self, msg):
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
        # self.statusBar().showMessage("就绪！")

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
            self.showConfidence()
        elif self.sender().objectName() == "toQueryButton":    
            self.__ui.rightTabWidget.setCurrentIndex(1)
            self.hideConfidence()
        elif self.sender().objectName() == "toShowTaskButton":
            self.__ui.rightTabWidget.setCurrentIndex(2)
            self.showConfidence()
    
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
            print(self.modelPath)
            print(self.yoloConfig['detectAnsPath'])
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
            self.taskList.append(FolderTask(id, imageFolderPath))
            self.taskList[id].thread.startSignal.connect(self.showMassage)
            self.taskList[id].thread.fileListSignal.connect(self.searchFinish)
            self.taskList[id].thread.start()
            
    # 文件搜索完成后完成文件列表的构建
    def searchFinish(self, fileList, id):
        self.taskList[id].finishBuild(fileList)
        self.changeTaskListSignal.emit()
        # self.statusBar().showMessage("就绪！")
    
    # 点击cameraButton按钮,选择摄像设备
    def clickcameraButton(self):
        # self.__ui.outImage.setImage(QPixmap('d:/vscode background/1.jpg'))
        pass    
        
    # 点击putAwayButton按钮隐藏右侧选项
    def clickPutAwayButton(self):
        self.__ui.leftGroupBox.hide()
        self.__ui.expandButton.show()
    # 点击expandButton按钮显示右侧选项
    def clickExpandButton(self):
        self.__ui.leftGroupBox.show()
        self.__ui.expandButton.hide()
    
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
        imageName = self.__ui.fileListTableList.item(row, 0).text()
        self.showImageDialog = ShowImageDialog(self.__ui.fileListTableList, row)
        # self.showImageDialog.exec()
        
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
            self.taskList[self.runindex].stop()
            # 提示是否停止该任务
            clossMessageBox = QMessageBox.question(self, '确认', '你确定要删除该任务?', 
                                               QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if clossMessageBox == QMessageBox.Yes:
                self.taskList[self.runindex].delTask()
            else:
                self.taskList[self.runindex].continues()
    
    # 点击stopButton时, 暂停或开始任务
    def clickStopButton(self):
        if self.__ui.stopButton.text() == "暂停":
            self.taskList[self.runindex].stop()
            self.__ui.stopButton.setText("继续")
        else:
            self.taskList[self.runindex].continues()
            self.__ui.stopButton.setText("暂停")
    
    # 处理检测线程的状态信号
    def dealDetectState(self, msg):
        self.statusBar().showMessage(msg)
        if (msg == "准备中"):
            self.__ui.enterButton.setEnabled(False)
            self.__ui.stopButton.setEnabled(False)
        elif (msg == "检测中"):
            self.__ui.enterButton.setEnabled(True)
            self.__ui.stopButton.setEnabled(True)
        elif (msg == "检测完成") or (msg == "用户取消"):
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
            
    # 接受传回的检测信息
    def receiveDetectInfo(self, detectInfo):
        self.finishNum += 1
        self.detectInfoList.append(detectInfo)
        # 如果正在查看任务文件列表, 刷新
        if self.runindex == self.showFileIndex and not self.__ui.fileListTableList.isHidden():
            self.runingFileList()
        self.readImageNum += 1
        if detectInfo.isHaveFlaw:
            self.flawNum += 1
        else:
            self.noFlawNum += 1
        self.__ui.currentNum.setText(str(self.readImageNum))
        self.__ui.standNum.setText(str(self.noFlawNum))
        self.__ui.flawNum.setText(str(self.flawNum))
        if (self.readImageNum == 1):
            self.showHome(self.showHomeIndex)
    
    # 主页显示瓷砖
    def showHome(self, index):
        # tmpThread = loadHomeImage(self.detectInfoList[index], self.__ui.inputImage, 
        #                           self.__ui.outImage, self.yoloConfig['confidence'], self.colorDict)
        # tmpThread.finishSignal.connect(self.finishLoadHomeImage)
        # self.loadHomeImageQueue.add(tmpThread)
        self.detectInfoList[index].setConfidence(self.yoloConfig['confidence'])
        self.__ui.outImage.setImage(self.detectInfoList[index].draw(self.colorDict))
        self.__ui.inputImage.setImage(QPixmap(self.detectInfoList[index].path))
        self.__ui.sideNum.setText(str(self.detectInfoList[index].flawStatistics['edge_anomaly']))
        self.__ui.angleNum.setText(str(self.detectInfoList[index].flawStatistics['corner_anomaly']))
        self.__ui.whiteNum.setText(str(self.detectInfoList[index].flawStatistics['white_point_blemishes']))
        self.__ui.lightNum.setText(str(self.detectInfoList[index].flawStatistics['light_block_blemishes']))
        self.__ui.darkNum.setText(str(self.detectInfoList[index].flawStatistics['dark_spot_blemishes']))
        self.__ui.apertureNum.setText(str(self.detectInfoList[index].flawStatistics['aperture_blemishes']))
    
    
    # 加载主页图像完成后
    # def finishLoadHomeImage(self):
    #     self.loadHomeImage_ = self.loadHomeImageQueue.delWork()
    # 鼠标双击切换显示图像
    def swapShowImage(self, msg):
        if msg == "inputImage":
            if self.showHomeIndex - 1 < 0:
                return
            else:
                self.showHomeIndex -= 1
        elif msg == "outImage":
            if self.showHomeIndex + 1 >= self.readImageNum:
                return
            else:
                self.showHomeIndex += 1
        self.showHome(self.showHomeIndex)
        