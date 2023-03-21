from PyQt5.Qt import QThread
import os
from utils.utilsDetect import detectImage

class DetectDirThread(QThread):
    def __init__(self, window) -> None:
        super().__init__()
        self._window = window
        # 获取图像文件列表
        self._imageList = [fileName for fileName in os.listdir(self._window.imageFolderPath)
                           if any(fileName.endswith(extension) for extension in self._window.includedExtensions)]
    def run(self):
        # 设置状态栏
        self._window.statusBar().showMessage("正在识别(文件夹)...")
        self._window.progressBar.setRange(0, len(self._imageList) - 1)
        self._window.progressBar.reset()
        # 图像识别
        for step, fileName in enumerate(self._imageList):
            print(step + 1, " :", fileName)
            detectImage(self._window.imageFolderPath, fileName, self._window.imageShape,
                        self._window.model, self._window.xmlPath,
                        self._window.classesDict)
            self._window.progressBar.setValue(step)
        # 设置状态栏
        self._window.statusBar().showMessage("就绪！")
        