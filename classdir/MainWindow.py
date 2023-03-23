from PyQt5.QtWidgets import QMainWindow, QColorDialog, QDialog, QFileDialog, QAbstractItemView, QTableWidgetItem, QMessageBox#, QProgressBar
from PyQt5.QtCore import pyqtSignal
from classdir.Ui_Window import Ui_MainWindow
# import pathlib
from utils.utilsXml import loadConfig
import os
from classdir.Worker import *
from classdir.Dialog import SettingDialog
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
    def __init__(self):
        super(MainWindow, self).__init__()
        # 界面初始化
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        # 设置隐藏QTabWidget的标签
        self._ui.rightTabWidget.tabBar().hide()
        # 初始化TableWidget
        self.initTableWidget()
        # 连接信号和槽
        self.connectSignalAndSlot()
        # 初始化窗口
        self.initWindow()
        # 设置状态栏
        self.statusBar().showMessage("就绪！")
    
    # 连接信号和槽
    def connectSignalAndSlot(self):
        self._ui.toHomeButton.clicked.connect(self.swapInterface)
        self._ui.toQueryButton.clicked.connect(self.swapInterface)
        self._ui.toShowTaskButton.clicked.connect(self.swapInterface)
        self._ui.confidenceNum.valueChanged.connect(self.changeConfidenceSlider)
        self._ui.confidenceSlider.valueChanged.connect(self.changeConfidenceSpinbox)
        self._ui.widthNum.valueChanged.connect(self.changeWidth)
        self._ui.heightNum.valueChanged.connect(self.changeHeight)
        self._ui.sideColor.clickSignal.connect(self.changeColor)
        self._ui.angleColor.clickSignal.connect(self.changeColor)
        self._ui.darkColor.clickSignal.connect(self.changeColor)
        self._ui.lightColor.clickSignal.connect(self.changeColor)
        self._ui.apertureColor.clickSignal.connect(self.changeColor)
        self._ui.whiteColor.clickSignal.connect(self.changeColor)
        self._ui.settingButton.clicked.connect(self.clickSettingButton)
        self._ui.fileButton.clicked.connect(self.clickfileButton)
        self._ui.folderButton.clicked.connect(self.clickfolderButton)
        self._ui.cameraButton.clicked.connect(self.clickcameraButton)
        self._ui.expandButton.clicked.connect(self.clickExpandButton)
        self._ui.putAwayButton.clicked.connect(self.clickPutAwayButton)
        self.changeTaskListSignal.connect(self.responseChangeTaskList)
        self._ui.taskQenueTableList.cellDoubleClicked.connect(self.delTask)
    # 初始化窗口
    def initWindow(self):
        # 加载配置文件
        config = loadConfig()
        # yolo输入图像尺寸
        self.imageShape = config['imageShape']
        # yolo模型目录
        self.modelPath = config['modelPath']
        # 置信度
        self.confidence = config['confidence']
        # 识别结果存放目录(如果没有该目录就创建)
        self.detectAnsPath = config['detectAnsPath']
        if not os.path.isdir(self.detectAnsPath):
            os.mkdir(self.detectAnsPath)    
        # 非极大抑制所用到的nms_iou大小
        self.nms_iou = config['nms_iou']       
        # 设置最大框的数量
        self.maxBoxes = config['maxBoxes']      
        # 该变量用于控制是否使用letterbox_image对输入图像进行不失真的resize
        self.letterboxImage = config['letterboxImage']
        # 瑕疵颜色字典
        self.colorDict = config['color']
        # 加载所有模型文件
        self.loadModelFile()
        # 设置瑕疵颜色
        (b, g, r) = self.colorDict['edge anomaly']
        self._ui.sideColor.setStyleSheet('font: 150 14pt "Agency FB";color:rgb' + str((r, g, b)) + ";")
        (b, g, r) = self.colorDict['corner anomaly']
        self._ui.angleColor.setStyleSheet('font: 150 14pt "Agency FB";color:rgb' + str((r, g, b)) + ";")
        (b, g, r) = self.colorDict['white point blemishes']
        self._ui.whiteColor.setStyleSheet('font: 150 14pt "Agency FB";color:rgb' + str((r, g, b)) + ";")
        (b, g, r) = self.colorDict['light block blemishes']
        self._ui.lightColor.setStyleSheet('font: 150 14pt "Agency FB";color:rgb' + str((r, g, b)) + ";")
        (b, g, r) = self.colorDict['dark spot blemishes']
        self._ui.darkColor.setStyleSheet('font: 150 14pt "Agency FB";color:rgb' + str((r, g, b)) + ";")
        (b, g, r) = self.colorDict['aperture blemishes']    
        self._ui.apertureColor.setStyleSheet('font: 150 14pt "Agency FB";color:rgb' + str((r, g, b)) + ";")
        # 纠正界面上输入图像的宽和高,置信度
        self._ui.widthNum.setValue(self.imageShape[0])
        self._ui.heightNum.setValue(self.imageShape[1])
        self._ui.confidenceNum.setValue(self.confidence)
        # 初始化按钮
        self._ui.toHomeButton.hide()
        self._ui.enterButton.setText("请添加任务")
        self._ui.enterButton.setEnabled(False)
        self._ui.stopButton.setText("暂停")
        self._ui.stopButton.hide()
        self._ui.toShowTaskButton.setText("任务队列")
        self._ui.toShowTaskButton.hide()
        self._ui.expandButton.hide()
    # 初始化TableWidget
    def initTableWidget(self):
        # 设置表格不可更改
        self._ui.queryTableList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._ui.taskQenueTableList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self._ui.fileListTableList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 设置表格行数(0行)
        self._ui.queryTableList.setRowCount(0)
        self._ui.taskQenueTableList.setRowCount(0)
        self._ui.fileListTableList.setRowCount(0)
        # 设置结果查询整行选择
        self._ui.queryTableList.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 设置结果查询显示行、列标题
        self._ui.queryTableList.horizontalHeader().setVisible(True)
        self._ui.queryTableList.verticalHeader().setVisible(True)
        self._ui.taskQenueTableList.horizontalHeader().setVisible(True)
        self._ui.taskQenueTableList.verticalHeader().setVisible(True)
        self._ui.fileListTableList.horizontalHeader().setVisible(True)
        self._ui.fileListTableList.verticalHeader().setVisible(True)
        # 设置文件列表隐藏
        self._ui.fileListTableList.hide()
        self._ui.fileListLabel.hide()
        self._ui.fileExpandButton.hide()
        
    # 修改配置文件
    def resiveConfigFile(self, key, vaule, secondKey=None):
        tmpThread = saveConfig(key, vaule, secondKey)
        tmpThread.saveConfigSignal.connect(self.checkResiveConfigQueue)
        self.resiveConfigQueue.add(tmpThread)
    
    # 配置文件修改完成后, 检查resiveConfigQueue
    def checkResiveConfigQueue(self):
        # 防止 Destroyed while thread is still running, 暂存前一个线程
        self.resiveConfigThread_ = self.resiveConfigQueue.delWork()
    # 加载模型文件
    def loadModelFile(self):
        self.modelList = [fileName for fileName in os.listdir(self.modelPath)
                          if any(fileName.endswith(extension) for extension in ['h5'])]
        self._ui.modelComboBox.clear()
        self._ui.modelComboBox.addItems(self.modelList) 
    
    # 页面切换    
    def swapInterface(self):
        self.sender().hide()
        index = self._ui.rightTabWidget.currentIndex()
        if index == 0:
            self._ui.toHomeButton.show()
        elif index == 1:
            self._ui.toQueryButton.show()
        else:
            self._ui.toShowTaskButton.show()
        if self.sender().objectName() == "toHomeButton":
            self._ui.rightTabWidget.setCurrentIndex(0)
        elif self.sender().objectName() == "toQueryButton":    
            self._ui.rightTabWidget.setCurrentIndex(1)
        elif self.sender().objectName() == "toShowTaskButton":
            self._ui.rightTabWidget.setCurrentIndex(2)
    # 置信度设置
    def changeConfidenceSpinbox(self):
        vaule = self._ui.confidenceSlider.value()
        self.confidence = vaule / 100
        self._ui.confidenceNum.setValue(self.confidence)
        self.resiveConfigFile('confidence', str(vaule / 100))
    def changeConfidenceSlider(self):
        vaule = self._ui.confidenceNum.value()
        self.confidence = vaule
        self._ui.confidenceSlider.setValue(int(self.confidence * 100))
        self.resiveConfigFile('confidence', str(vaule))

    # 宽设置
    def changeWidth(self):
        vaule = self._ui.widthNum.value()
        if (vaule % 32 != 0):
            vaule = int(vaule / 32 + 0.5) * 32
        self.imageShape[0] = vaule
        self._ui.widthNum.setValue(vaule)
        self.resiveConfigFile('imageShape', str(vaule), 'width')
        
    # 高设置
    def changeHeight(self):
        vaule = self._ui.heightNum.value()
        if (vaule % 32 != 0):
            vaule = int(vaule / 32 + 0.5) * 32
        self.imageShape[1] = vaule
        self._ui.heightNum.setValue(vaule)
        self.resiveConfigFile('imageShape', str(vaule), 'height')

    # 设置瑕疵标记颜色
    def changeColor(self, msg):
        color = QColorDialog.getColor()
        if color.isValid():
            if msg == 'edge_anomaly':
                label = self._ui.sideColor
            elif msg == 'aperture_blemishes':
                label = self._ui.apertureColor
            elif msg == 'dark_spot_blemishes':
                label = self._ui.darkColor
            elif msg == 'light_block_blemishes':
                label = self._ui.lightColor
            elif msg == 'white_point_blemishes':
                label = self._ui.whiteColor
            elif msg == 'corner_anomaly':
                label = self._ui.angleColor
            self.resiveConfigFile(msg, str((color.blue(), color.green(), color.red())))
            label.setStyleSheet('font: 150 14pt "Agency FB";color:' + color.name() + ";")
    
    # 点击setting按钮
    def clickSettingButton(self):
        self.settingDialog = SettingDialog(self.modelPath, self.detectAnsPath,
                                     self.nms_iou, self.maxBoxes, self.letterboxImage)
        # 如果点击确定, 修改相关参数和配置文件
        if self.settingDialog.exec() == QDialog.Accepted:
            # 修改模型路径，并加载该路径下的模型
            self.modelPath = self.settingDialog.ui.modelPathEdit.text()
            self.resiveConfigFile('modelPath', self.modelPath)
            self.loadModelFile()
            # 修改检测结果存放位置
            self.detectAnsPath = self.settingDialog.ui.detecAnsPathEdit.text()
            self.resiveConfigFile('detectAnsPath', self.detectAnsPath)
            # 修改nms_iou
            self.nms_iou = self.settingDialog.ui.nms_iouNum.value()
            self.resiveConfigFile('nms_iou', str(self.nms_iou))
            # 修改最大框的数量
            self.maxBoxes = self.settingDialog.ui.maxBoxesNum.value()
            self.resiveConfigFile('maxBoxes', str(self.maxBoxes))
            # 修改letterboxImage
            self.letterboxImage = self.settingDialog.ui.letterboxImageCheckBox.isChecked()
            self.resiveConfigFile('letterboxImage', str(self.letterboxImage))
        
    
    # 点击fileButton按钮
    def clickfileButton(self):
        imageFileList, ok= QFileDialog.getOpenFileNames(self,'选择图像', os.getcwd(),'Image files ' + 
            str(tuple([('*.' + extensions) for extensions in self.includedExtensions])).replace("'", "").replace(",", ""))
        if (ok):
            id = len(self.taskList)
            self.taskList.append(FilesTask(id, imageFileList))
            self.changeTaskListSignal.emit()

    # 点击folderButton按钮
    def clickfolderButton(self):
        imageFolderPath = QFileDialog.getExistingDirectory(
                self, "选择文件夹", os.getcwd()) + "/"
        if (imageFolderPath != '/'):
            id = len(self.taskList)
            self.taskList.append(FolderTask(id, imageFolderPath))
            self.changeTaskListSignal.emit()

    # 点击cameraButton按钮
    def clickcameraButton(self):
        pass    
        
    # 点击putAwayButton按钮
    def clickPutAwayButton(self):
        self._ui.leftGroupBox.hide()
        self._ui.expandButton.show()
    # 点击expandButton按钮
    def clickExpandButton(self):
        self._ui.leftGroupBox.show()
        self._ui.expandButton.hide()
    
    # 响应taskList变化
    # taskList变化时重新加载taskQenueTableList
    def responseChangeTaskList(self):
        row = []
        for (step, task) in enumerate(self.taskList):
            if task.isValid:
                row.append(step)
        countRow = len(row)
        if countRow == 0:
            self._ui.toShowTaskButton.hide()
            self._ui.enterButton.setText("请添加任务")
            self._ui.enterButton.setEnabled(False)
            self._ui.rightTabWidget.setCurrentIndex(0)
            self._ui.toHomeButton.hide()
        else:
            # 设置taskQenueTableList行数
            self._ui.taskQenueTableList.setRowCount(countRow)
            for (step, index) in enumerate(row):
                self._ui.taskQenueTableList.setItem(step, 0, QTableWidgetItem(self.taskList[index].name))
                self._ui.taskQenueTableList.setItem(step, 1, QTableWidgetItem(str(index)))
            self._ui.toShowTaskButton.show()
            if (self._ui.enterButton.text() == "请添加任务"):
                self._ui.enterButton.setText("开始检测")
                self._ui.enterButton.setEnabled(True)
    
    # 双击删除任务
    def delTask(self, row):
        reply = QMessageBox.question(self, '删除任务', '确定要删除该任务？',
                             QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
        
        if (reply == QMessageBox.Yes):
            self.taskList[int(self._ui.taskQenueTableList.item(row, 1).text())].delTask()
            self.changeTaskListSignal.emit()
    
    # 点击显示文件列表