from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from classdir.Ui_Setting import Ui_SettingDialog
from classdir.Ui_ShowImage import Ui_ShowImageDialog
import os


class SettingDialog(QDialog):
    def __init__(self, modelPath, detecAnsPath, nms_iou, maxBoxes, letterboxImage) -> None:
        super(SettingDialog, self).__init__()
        # 设置显示关闭按钮, 最小化按钮
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowModality(Qt.ApplicationModal)
        # 界面初始化
        self.ui = Ui_SettingDialog()
        self.ui.setupUi(self)
        # 初始化参数
        self.ui.modelPathEdit.setText(modelPath)
        self.ui.detecAnsPathEdit.setText(detecAnsPath)
        self.ui.nms_iouNum.setValue(nms_iou)
        self.ui.maxBoxesNum.setValue(maxBoxes)
        self.ui.letterboxImageCheckBox.setChecked(letterboxImage)
        # 连接信号和槽
        self.ui.buttonBox.accepted.connect(self.clickAcceptButton)
        self.ui.modelButton.clicked.connect(self.clickModelButton)
        self.ui.detecAnsPathButton.clicked.connect(self.clickDetecAnsPathButton)
        # 窗口显示
        self.show()
    # 点击确定时检查路径
    def clickAcceptButton(self):
        self.ui.modelPathEdit.setText(self.ui.modelPathEdit.text().replace('\\', '/'))
        self.ui.detecAnsPathEdit.setText(self.ui.detecAnsPathEdit.text().replace('\\', '/'))
        if not os.path.isdir(self.ui.modelPathEdit.text()):
            QMessageBox.critical(self,'Error','请检测模型路径是否正确!!!',QMessageBox.Ok)
            return
        if not os.path.isdir(self.ui.detecAnsPathEdit.text()):
            QMessageBox.critical(self,'Error','请检测检测结果路径是否正确!!!',QMessageBox.Ok)
            return
        self.accept()
    # 选择模型位置
    def clickModelButton(self):
        modelPath = QFileDialog.getExistingDirectory(
                 self, "选择模型位置", os.getcwd())
        if modelPath != "":
            self.ui.modelPathEdit.setText(modelPath)
    # 选择检测结果存放位置
    def clickDetecAnsPathButton(self):
        detecAnsPath = QFileDialog.getExistingDirectory(
                 self, "选择检测结果存放位置", os.getcwd())
        if detecAnsPath != "":
            self.ui.detecAnsPathEdit.setText(detecAnsPath)


class ShowImageDialog(QDialog):
    def __init__(self, fileListTableList, row) -> None:
        super(ShowImageDialog, self).__init__()
        # 设置显示关闭按钮, 最小化按钮
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint)
        # 界面初始化
        self.ui = Ui_ShowImageDialog()
        self.ui.setupUi(self)
        self.fileListTableList = fileListTableList
        # 文件列表长度
        self.len = self.fileListTableList.rowCount()
        # 当前文件
        self.row = row
        # 获取文件名
        imageName = self.fileListTableList.item(self.row, 0).text()
        # 连接信号和槽
        self.ui.reduceButton.clicked.connect(self.clickReduceButton)
        self.ui.amplifyButton.clicked.connect(self.clickAmplifyButton)
         # 窗口显示
        self.show()
        # 设置图像和标题
        self.ui.graphicsView.loadImage(QPixmap(imageName))
        self.ui.nameLabel.setText(imageName.split("/")[-1])
    # 前一张图像
    def clickAmplifyButton(self):
        if self.row + 1 < self.len:
            self.row += 1
            imageName = self.fileListTableList.item(self.row, 0).text()
            self.ui.graphicsView.setImage(QPixmap(imageName))
            self.ui.nameLabel.setText(imageName.split("/")[-1])
    # 后一张图像
    def clickReduceButton(self):
        if self.row - 1 >= 0:
            self.row -= 1
            imageName = self.fileListTableList.item(self.row, 0).text()
            self.ui.graphicsView.setImage(QPixmap(imageName))
            self.ui.nameLabel.setText(imageName.split("/")[-1])

        
    