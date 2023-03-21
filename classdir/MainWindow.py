from PyQt5.QtWidgets import QMainWindow, QFileDialog, QProgressBar
from classdir.Ui_Window import Ui_MainWindow
# from classdir.Query import Ui_QueryUI
from classdir.Worker import DetectDirThread
from classdir.Yolo import YOLO
import os

class MainWindow(QMainWindow):
    xmlPath = 'xmlpath/'
    _imageFolderPath = "C:/Users"
    def __init__(self):
        super(MainWindow, self).__init__()
        self._ui = Ui_MainWindow()
        self._ui.setupUi(self)
        self._ui.pushButton.clicked.connect(self.showChild)
        self._ui.fileButton.clicked.connect(self.openFolder)
        self.statusBar().showMessage("就绪！")
        self._ui.tabWidget.tabBar().hide()
        self.progressBar = QProgressBar(self, textVisible=True)
        self.progressBar.setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 5px; color: rgb(0, 0, 0);  \
                                        background-color: #FFFFFF; text-align: center;} \
                                        QProgressBar::chunk {background-color: rgb(0, 255, 0); \
                                        border-radius: 10px; margin: 0.1px;  width: 1px;}")
        self.progressBar.resize(300, 20)
        self.statusBar().addPermanentWidget(self.progressBar)
        self.imageShape = [832, 608]
        self.model = YOLO(self.imageShape)
    def showChild(self):
        # self.show()
        self._ui.tabWidget.setCurrentIndex(1)
        
    def openFolder(self):
        self._imageFolderPath = QFileDialog.getExistingDirectory(
            self, "选择文件夹", self._imageFolderPath) + "/"
        self.startDetectDir()
        
    def startDetectDir(self):
        self.thread_1 = DetectDirThread(self._imageFolderPath, self)
        self.thread_1.start()
        

        