
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