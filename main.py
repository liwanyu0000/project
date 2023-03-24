import sys
from PyQt5.QtWidgets import QApplication
from classdir.MainWindow import MainWindow
from PyQt5.QtGui import QPixmap

from classdir.Dialog import *

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
