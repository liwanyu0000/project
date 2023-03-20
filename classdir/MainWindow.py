from PyQt5.QtWidgets import QMainWindow
from classdir.Home import Ui_MainWindow
from classdir.Query import Ui_QueryUI

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.showChild)
        self.QuerUI =  Ui_QueryUI()
        self.QuerUI.setupUi(self.QuerUI)
    def showChild(self):
        self.QuerUI.show()