from PyQt5.QtWidgets import QMainWindow, QFileDialog, QProgressBar
from classdir.Ui_Window import Ui_MainWindow
from classdir.Worker import DetectDirThread
from classdir.Yolo import YOLO
import pathlib
from utils.utilsXml import loadConfig
import os

class MainWindow(QMainWindow):
    # 支持的图像格式列表
    includedExtensions = ['jpg', 'jpeg', 'bmp', 'png', 'dib', 'jpe', 'pbm', 'pgm', 'ppm', 'tiff', 'tif']
    # 文件夹目录
    imageFolderPath = str(pathlib.Path.home())
    # 瑕疵类别字典
    classesDict = {0 : 'edge anomaly',
                   1 : 'corner anomaly',
                   2 : 'white point blemishes',
                   3 : 'light block blemishes',
                   4 : 'dark spot blemishes',
                   5 : 'aperture blemishes'}
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init()
        
        # 设置状态栏
        self.statusBar().showMessage("就绪！")
        # self.progressBar = QProgressBar(self, textVisible=True)
        # self.progressBar.setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 5px; color: rgb(0, 0, 0);  \
        #                                 background-color: #FFFFFF; text-align: center;} \
        #                                 QProgressBar::chunk {background-color: rgb(0, 255, 0); \
        #                                 border-radius: 10px; margin: 0.1px;  width: 1px;}")
        # self.statusBar().addPermanentWidget(self.progressBar)
        
        # 设置隐藏QTabWidget的标签
        self._ui.rightTabWidget.tabBar().hide()
        
        # 注册
        self._ui.swapButton.clicked.connect(self.swapInterface)
        self._ui.folderButton.clicked.connect(self.openFolder)
    
    # 初始化程序
    def init(self):
        # 界面初始化
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        # 加载配置文件
        config = loadConfig()
        # yolo输入图像尺寸
        self.imageShape = config['imageShape']
        # yolo模型目录
        self.modelPath = config['modelPath']
        # 置信度
        self.confidence = config['confidence']
        # 识别结果存放目录(如果没有该目录就创建)
        self.detectAnsDir = config['detectAnsDir']
        if not os.path.isdir(self.detectAnsDir):
            os.mkdir(self.detectAnsDir)    
        # 非极大抑制所用到的nms_iou大小
        self.nms_iou = config['nms_iou']       
        # 设置最大框的数量
        self.maxBoxes = config['maxBoxes']      
        # 该变量用于控制是否使用letterbox_image对输入图像进行不失真的resize
        self.letterboxImage = config['letterboxImage']
        # 瑕疵颜色字典
        self.colorDict = config['color']
        # 初始化yolo模型
        self.model = YOLO(self.imageShape)
        # 修改参数
        self.model.setYolo(
            nms_iou=self.nms_iou,
            maxBoxes=self.maxBoxes,
            letterboxImage=self.letterboxImage)
        # 加载界面内容
        # 加载所有模型文件
        self.modelList = [fileName for fileName in os.listdir(self.modelPath)
                          if any(fileName.endswith(extension) for extension in ['h5'])]
        self._ui.modelComboBox.clear()
        self._ui.modelComboBox.addItems(self.modelList)  
        # 设置使用的权重文件
        modelFile = self.modelPath + self._ui.modelComboBox.currentText()
        self.model.setModelPath(modelFile, modelFile[-4])
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
        
        # 纠正输入图像的宽和高,置信度
        self._ui.widthNum.setValue(self.imageShape[0])
        self._ui.hightNum.setValue(self.imageShape[1])
        self._ui.confidenceNum.setValue(self.confidence)

        
        
        
    
    # 页面切换    
    def swapInterface(self):
        if self._ui.swapButton.text() == "结果查询":
            self._ui.rightTabWidget.setCurrentIndex(1)
            self._ui.swapButton.setText("主页")
        else:
            self._ui.rightTabWidget.setCurrentIndex(0)
            self._ui.swapButton.setText("结果查询")
    
    # 选择文件夹    
    def openFolder(self):
            self.imageFolderPath = QFileDialog.getExistingDirectory(
                self, "选择文件夹", self.imageFolderPath) + "/"
            if (self.imageFolderPath != '/'):
                # self.startDetectDir()
                pass
            else:
                self.imageFolderPath = str(pathlib.Path.home())
        
    # 识别文件夹   
    def startDetectDir(self):
        try:
            self.threadDetectDir = DetectDirThread(self)
            self.threadDetectDir.start()   
        except Exception as r:
            print('未知错误 %s' %(r))    