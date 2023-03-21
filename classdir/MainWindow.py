from PyQt5.QtWidgets import QMainWindow, QFileDialog, QProgressBar
from classdir.Ui_Window import Ui_MainWindow
from classdir.Worker import DetectDirThread
from classdir.Yolo import YOLO
import pathlib

class MainWindow(QMainWindow):
    # 识别结果存放目录
    xmlPath = 'xmlpath/'
    # 支持的图像格式列表
    includedExtensions = ['jpg', 'jpeg', 'bmp', 'png', 'dib', 'jpe', 'pbm', 'pgm', 'ppm', 'tiff', 'tif']
    # 文件夹目录
    imageFolderPath = str(pathlib.Path.home())
    # yolo输入图像尺寸
    imageShape = [832, 608]
    # 瑕疵类别字典
    classesDict = {0 : 'edge anomaly',
                   1 : 'corner anomaly',
                   2 : 'white point blemishes',
                   3 : 'light block blemishes',
                   4 : 'dark spot blemishes',
                   5 : 'aperture blemishes'}
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        
        # 设置状态栏
        self.statusBar().showMessage("就绪！")
        self.progressBar = QProgressBar(self, textVisible=True)
        self.progressBar.setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 5px; color: rgb(0, 0, 0);  \
                                        background-color: #FFFFFF; text-align: center;} \
                                        QProgressBar::chunk {background-color: rgb(0, 255, 0); \
                                        border-radius: 10px; margin: 0.1px;  width: 1px;}")
        self.statusBar().addPermanentWidget(self.progressBar)
        
        # 设置隐藏QTabWidget的标签
        self._ui.tabWidget.tabBar().hide()
        
        # 创建yolo模型
        self.model = YOLO(self.imageShape)
        
        # 注册
        self._ui.pushButton.clicked.connect(self.showChild)
        self._ui.fileButton.clicked.connect(self.openFolder)
        
    def showChild(self):
        # self.show()
        self._ui.tabWidget.setCurrentIndex(1)
    
    # 选择文件夹    
    def openFolder(self):
            self.imageFolderPath = QFileDialog.getExistingDirectory(
                self, "选择文件夹", self.imageFolderPath) + "/"
            if (self.imageFolderPath != '/'):
                self.startDetectDir()
            else:
                self.imageFolderPath = str(pathlib.Path.home())
        
    # 识别文件夹   
    def startDetectDir(self):
        try:
            self.threadDetectDir = DetectDirThread(self)
            self.threadDetectDir.start()   
        except Exception as r:
            print('未知错误 %s' %(r))    