from PyQt5.Qt import QThread
import os
from utils.utilsDetect import detectImage

class DetectDirThread(QThread):
    def __init__(self, imageDir, window) -> None:
        super().__init__()
        self._imageDir = imageDir
        self._imageList = os.listdir(imageDir)
        self._window = window
    def run(self):
        self._window.statusBar().showMessage("正在识别(文件夹)...")
        self._window.progressBar.setRange(0, len(self._imageList) - 1)
        self._window.progressBar.reset()
        for step, fileName in enumerate(self._imageList):
            detectImage(self._imageDir, fileName, self._window.imageShape,
                        self._window.model, self._window.xmlPath,
                        {
                            0 : 'edge_anomaly',
                            1 : 'corner_anomaly',
                            2 : 'white_point_blemishes',
                            3 : 'light_block_blemishes',
                            4 : 'dark_spot_blemishes',
                            5 : 'aperture_blemishes'
                        })
            self._window.progressBar.setValue(step)
        self._window.statusBar().showMessage("就绪！")