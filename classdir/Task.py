import os
from classdir.Worker import SearchFile, DetectThread

class Task(object):
    # 支持的图像格式列表
    includedExtensions = ['jpg', 'jpeg', 'bmp', 'png', 'dib', 'jpe', 'pbm', 'pgm', 'ppm', 'tiff', 'tif']
    # 文件列表
    fileList = []
    # 已完成文件数量
    finishFileNum = 0
    def __init__(self, id, arg) -> None:
        # id为任务列表的索引
        self.id = id
        # 记录任务是否有效
        self.isValid = True
        self.isStart = False
        self.buildFileList(arg)
    # 使任务失效
    def delTask(self):
        self.isValid = False
    # 构建任务列表
    def buildFileList(self, arg):
        pass
    # 开始识别
    def start(self, yoloConfig:dict):
        self.isStart = True
        self.fileNum = len(self.fileList)
        # 创建识别线程
        self.detectThread = DetectThread(yoloConfig, self.fileList)
        return self.fileNum
    # 更新文件列表
    def updateFileList(self, number=1):
        self.fileList = self.fileList[number:]
        self.finishFileNum += number
    def save(self):
        pass
class FilesTask(Task):
    def __init__(self, id, fileList) -> None:
        super().__init__(id, fileList)
        self.name = "检测文件"
    def buildFileList(self, fileList):
        self.fileList = fileList
        return super().buildFileList(fileList)
    def save(self):
        vaule = "files"
        for file in self.fileList:
            vaule = vaule + ";" + file
        return vaule

class FolderTask(Task):
    def __init__(self, id, folder) -> None:
        super().__init__(id, folder)
        self.folder = folder
        self.name = "检测'" + folder +"'文件夹"
    def buildFileList(self, folder):
        self.thread = SearchFile(folder, self.includedExtensions, self.id)
        return super().buildFileList(folder)
    def finishBuild(self, fileList):
        if (len(fileList) == 0):
            self.delTask()
            return
        self.fileList = fileList
    def save(self):
        vaule = "folder;" + str(self.finishFileNum) + ";" + self.folder
        return vaule
    
class LoadTask():
    def __init__(self, id, arg) -> None:
        self.id = id
        self.arg = arg
    def load(self):
        taskInfo = self.arg.split(';')
        if taskInfo[0] == 'files':
            return FilesTask(self.id, taskInfo[1:])
        elif taskInfo[0] == 'folder':
            tmp = FolderTask(self.id, taskInfo[2])
            tmp.updateFileList(int(taskInfo[1]))
            return tmp
        