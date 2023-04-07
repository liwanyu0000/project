#-*-coding:utf-8-*-
import os
import sys
from PyQt5.QtWidgets import QApplication
from classdir.MainWindow import MainWindow
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "4"
os.environ["AUTOGRAPH_VERBOSITY"] = "1"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())