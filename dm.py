
        # 初始化yolo模型
        # self.model = YOLO(self.imageShape)
        # 修改参数
        # self.model.setYolo(
        #     nms_iou=self.nms_iou,
        #     maxBoxes=self.maxBoxes,
        #     letterboxImage=self.letterboxImage)
        # 加载界面内容
        
        
        
        # 设置使用的权重文件
        # modelFile = self.modelPath + self._ui.modelComboBox.currentText()
        # self.model.setModelPath(modelFile, modelFile[-4])
        
            # 选择文件夹    
    # def openFolder(self):
    #         self.imageFolderPath = QFileDialog.getExistingDirectory(
    #             self, "选择文件夹", self.imageFolderPath) + "/"
    #         if (self.imageFolderPath != '/'):
    #             # self.startDetectDir()
    #             pass
    #         else:
    #             self.imageFolderPath = str(pathlib.Path.home())
        
    # 识别文件夹   
    # def startDetectDir(self):
    #     try:
    #         self.threadDetectDir = DetectDirThread(self)
    #         self.threadDetectDir.start()   
    #     except Exception as r:
    #         print('未知错误 %s' %(r))    
    
        # self.progressBar = QProgressBar(self, textVisible=True)
        # self.progressBar.setStyleSheet("QProgressBar { border: 2px solid grey; border-radius: 5px; color: rgb(0, 0, 0);  \
        #                                 background-color: #FFFFFF; text-align: center;} \
        #                                 QProgressBar::chunk {background-color: rgb(0, 255, 0); \
        #                                 border-radius: 10px; margin: 0.1px;  width: 1px;}")
        # self.statusBar().addPermanentWidget(self.progressBar)
        
# from PyQt5.Qt import QThread
# import os
# from utils.utilsDetect import detectImage

# class DetectDirThread(QThread):
#     def __init__(self, window) -> None:
#         super().__init__()
#         self._window = window
#         # 获取图像文件列表
#         self._imageList = [fileName for fileName in os.listdir(self._window.imageFolderPath)
#                            if any(fileName.endswith(extension) for extension in self._window.includedExtensions)]
#     def run(self):
#         # 设置状态栏
#         self._window.statusBar().showMessage("正在识别(文件夹)...")
#         self._window.progressBar.setRange(0, len(self._imageList) - 1)
#         self._window.progressBar.reset()
#         # 图像识别
#         for step, fileName in enumerate(self._imageList):
#             print(step + 1, " :", fileName)
#             detectImage(self._window.imageFolderPath, fileName, self._window.imageShape,
#                         self._window.model, self._window.xmlPath,
#                         self._window.classesDict)
#             self._window.progressBar.setValue(step)
#         # 设置状态栏
#         self._window.statusBar().showMessage("就绪！")

