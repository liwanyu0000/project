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

class MainWindow(QMainWindow):
    # 支持的图像格式列表
    includedExtensions = ['jpg', 'jpeg', 'bmp', 'png', 'dib', 'jpe', 'pbm', 'pgm', 'ppm', 'tiff', 'tif']
    # 瑕疵类别字典
    # classesDict = {0 : 'edge anomaly',
    #                1 : 'corner anomaly',
    #                2 : 'white point blemishes',
    #                3 : 'light block blemishes',
    #                4 : 'dark spot blemishes',
    #                5 : 'aperture blemishes'}
    # 修改配置文件的线程队列
    resiveConfigQueue = WorkQueue()
    # 任务列表
    taskList = []
    # 定义信号
    # 任务列表改动时发送信号
    changeTaskListSignal = pyqtSignal()
    # 正在执行的任务索引(无任务时为-1)
    runindex = -1
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
        # 初始化窗口
        self.__initWindow()
        # 设置状态栏
        self.statusBar().showMessage("就绪！")
    
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
        # tmpThread.
        self.resiveConfigQueue.add(tmpThread)
        
    # 开始修改配置文件时,显示消息
    def showMassage(self, msg):
        self.statusBar().showMessage(msg)
        
    # 配置文件修改完成后, 检查resiveConfigQueue
    def checkResiveConfigQueue(self):
        # 防止 Destroyed while thread is still running, 暂存前一个线程
        self.resiveConfigThread_ = self.resiveConfigQueue.delWork()
        self.statusBar().showMessage("就绪！")

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
        elif self.sender().objectName() == "toShowTaskButton":
            self.__ui.rightTabWidget.setCurrentIndex(2)
            
    # 置信度设置
    def changeConfidenceSpinbox(self):
        vaule = self.__ui.confidenceSlider.value()
        self.yoloConfig['confidence'] = vaule / 100
        self.__ui.confidenceNum.setValue(self.yoloConfig['confidence'])
        self.resiveConfigFile('confidence', str(vaule / 100))
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
    
    # 点击setting按钮, 打开设置子窗口
    def clickSettingButton(self):
        self.settingDialog = SettingDialog(self.modelPath, self.yoloConfig['detectAnsPath'],
                                     self.yoloConfig['nms_iou'], self.yoloConfig['maxBoxes'], 
                                     self.yoloConfig['letterboxImage'])
        # 如果点击确定, 修改相关参数和配置文件
        if self.settingDialog.exec() == QDialog.Accepted:
            # 修改模型路径，并加载该路径下的模型
            self.modelPath = self.settingDialog.ui.modelPathEdit.text()
            self.resiveConfigFile('modelPath', self.modelPath)
            self.loadModelFile()
            # 修改检测结果存放位置
            self.yoloConfig['detectAnsPath'] = self.settingDialog.ui.detecAnsPathEdit.text()
            self.resiveConfigFile('detectAnsPath', self.yoloConfig['detectAnsPath'])
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
            
    # 搜索完成后完成文件列表的构建
    def searchFinish(self, fileList, id):
        self.taskList[id].finishBuild(fileList)
        self.changeTaskListSignal.emit()
        self.statusBar().showMessage("就绪！")
    
    # 点击cameraButton按钮,选择摄像设备
    def clickcameraButton(self):
        self.__ui.outImage.loadImage(QPixmap('d:/vscode background/1.jpg'))
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
        fileList = self.taskList[int(self.__ui.taskQenueTableList.item(row, 1).text())].fileList
        countRow = len(fileList)
        # 如果列表中无文件，则说明搜索文件的线程未启动
        if (countRow) == 0:
            self.taskList[int(self.__ui.taskQenueTableList.item(row, 1).text())].thread.startSignal.connect(self.showMassage)
            self.taskList[int(self.__ui.taskQenueTableList.item(row, 1).text())].thread.fileListSignal.connect(self.searchFinish)
            self.taskList[int(self.__ui.taskQenueTableList.item(row, 1).text())].thread.start()
        else:
            self.__ui.fileListTableList.setRowCount(countRow)
            for (step, fileName) in enumerate(fileList):
                    self.__ui.fileListTableList.setItem(step, 0, QTableWidgetItem(fileName))
            self.__ui.fileExpandButton.show()
            self.__ui.fileListLabel.show()
            self.__ui.fileListTableList.show()
    
    # 点击
    def runingFileList(self):
        if self.runindex == -1:
            return
        fileList = self.taskList[self.runindex].fileList
        countRow = len(fileList)
        # 如果列表中无文件，则说明搜索文件的线程未启动
        if (countRow) == 0:
            self.taskList[self.runindex].thread.startSignal.connect(self.showMassage)
            self.taskList[self.runindex].thread.fileListSignal.connect(self.searchFinish)
            self.taskList[self.runindex].thread.start()
        else:
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
        self.showImageDialog = ShowImageDialog(QPixmap(imageName))
        self.showImageDialog.exec()
        
    # 点击enterButton时, 如果当前无识别任务，则开始识别, 否则取消当前任务
    def clickEnterButton(self):
        if self.__ui.enterButton.text() == '开始检测':
            # 获取taskQenueTableList中第一项在taskList中的索引
            self.runindex = int(self.__ui.taskQenueTableList.item(0, 1).text())
            # 获取当前选中的模型文件
            self.yoloConfig['modelFilePath'] = self.modelPath + self.__ui.modelComboBox.currentText()
            
            # 开始检测
            self.taskList[self.runindex].start(self.yoloConfig)
            # 改变按钮状态
            self.__ui.enterButton.setText("取消当前任务")
            self.__ui.stopButton.show()
            # 设置当前正在执行的任务
            self.__ui.runTaskInfoLabel.setText(self.__ui.taskQenueTableList.item(0, 0).text())
            # 把当前任务从taskQenueTableList中删除（发送信号即可）
            self.changeTaskListSignal.emit()