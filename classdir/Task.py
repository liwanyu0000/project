import os

class Task(object):
    # 支持的图像格式列表
    includedExtensions = ['jpg', 'jpeg', 'bmp', 'png', 'dib', 'jpe', 'pbm', 'pgm', 'ppm', 'tiff', 'tif']
    def __init__(self, id, arg) -> None:
        # id为任务列表的索引
        self.id = id
        # 记录任务是否有效
        self.isValid = True
        self.buildFileList(arg)
    # 修改id
    def updateId(self, id):
        self.id = id
    # 使任务失效
    def delTask(self):
        self.isValid = False
    # 构建任务列表
    def buildFileList(self, arg):
        pass
    # 开始识别
    def detect(self):
        pass
    
class FilesTask(Task):
    def __init__(self, id, fileList) -> None:
        super().__init__(id, fileList)
        self.name = "检测文件"
    def buildFileList(self, fileList):
        self.fileList = fileList
        return super().buildFileList(fileList)

class FolderTask(Task):
    def __init__(self, id, folder) -> None:
        super().__init__(id, folder)
        self.name = "检测'" + folder +"'文件夹"
    def buildFileList(self, folder):
        self.fileList = [folder + fileName for fileName in os.listdir(folder)
                if any(fileName.endswith(extension) for extension in self.includedExtensions)]
        if (len(self.fileList) == 0):
            self.delTask()
        return super().buildFileList(folder)