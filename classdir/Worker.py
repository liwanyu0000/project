from PyQt5.Qt import QThread
import os
from utils.utilsDetect import detectImage

class DetectDirThread(QThread):
    def __init__(self, window) -> None:
        super().__init__()
        self._window = window
        self._imageList = [fileName for fileName in os.listdir(self._window.imageFolderPath)
                           if any(fileName.endswith(extension) for extension in self._window.includedExtensions)]
    def run(self):
        self._window.statusBar().showMessage("正在识别(文件夹)...")
        self._window.progressBar.setRange(0, len(self._imageList) - 1)
        self._window.progressBar.reset()
        for step, fileName in enumerate(self._imageList):
            print(step + 1, " :", fileName)
            detectImage(self._window.imageFolderPath, fileName, self._window.imageShape,
                        self._window.model, self._window.xmlPath,
                        self._window.classesDict)
            self._window.progressBar.setValue(step)
        self._window.statusBar().showMessage("就绪！")
        