from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog
from PyQt5.QtCore import Qt
from classdir.Ui_Setting import Ui_SettingDialog
import os


class SettingDialog(QDialog):
    def __init__(self, modelPath, detecAnsPath, nms_iou, maxBoxes, letterboxImage) -> None:
        super(SettingDialog, self).__init__()
        self.accept
        # 设置显示关闭按钮, 最小化按钮
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
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
                 self, "选择模型位置", os.getcwd()) + '/'
        if modelPath != "/":
            self.ui.modelPathEdit.setText(modelPath)
    # 选择检测结果存放位置
    def clickDetecAnsPathButton(self):
        detecAnsPath = QFileDialog.getExistingDirectory(
                 self, "选择检测结果存放位置", os.getcwd()) + '/'
        if detecAnsPath != "/":
            self.ui.detecAnsPathEdit.setText(detecAnsPath)

        
    