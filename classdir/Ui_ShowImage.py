# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\liwan\Desktop\project\ui\ShowImage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from classdir.QtClass import ImageBox


class Ui_ShowImageDialog(object):
    def setupUi(self, ShowImageDialog):
        ShowImageDialog.setObjectName("ShowImageDialog")
        ShowImageDialog.resize(975, 751)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/熊猫.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ShowImageDialog.setWindowIcon(icon)
        ShowImageDialog.setStyleSheet("QWidget{\n"
"background-color: rgba(75, 75, 75, 0.3);\n"
"border: 0px solid #42adff;\n"
"border-radius:0px;}\n"
"QPushButton {\n"
"    font-size: 18px;\n"
"    font-family: \"Microsoft YaHei\";\n"
"    font-weight: bold;\n"
"     border-radius:9px;\n"
"    background:rgba(66, 195, 255, 0);\n"
"    color: rgb(218, 218, 218);\n"
"}\n"
"QPushButton:focus{\n"
"    outline: none;\n"
"}\n"
"QPushButton::pressed{\n"
"    font-family: \"Microsoft YaHei\";\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    color:rgb(200,200,200);\n"
"    text-align: center center;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    padding-top: 4px;\n"
"    padding-bottom: 4px;\n"
"    border-style: solid;\n"
"    border-width: 0px;\n"
"    border-color: rgba(255, 255, 255, 255);    \n"
"    border-radius: 3px;\n"
"    background-color:  #bf513b;\n"
"}\n"
"QPushButton::hover {\n"
"    border-style: solid;\n"
"    border-width: 0px;\n"
"    border-radius: 0px;\n"
"    background-color: rgba(48,148,243,80);\n"
"}")
        self.verticalLayout = QtWidgets.QVBoxLayout(ShowImageDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.graphicsView = ImageBox(ShowImageDialog)
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(40)
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.reduceButton = QtWidgets.QPushButton(ShowImageDialog)
        self.reduceButton.setMinimumSize(QtCore.QSize(50, 50))
        self.reduceButton.setMaximumSize(QtCore.QSize(50, 50))
        self.reduceButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/reduce.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reduceButton.setIcon(icon1)
        self.reduceButton.setIconSize(QtCore.QSize(40, 40))
        self.reduceButton.setObjectName("reduceButton")
        self.horizontalLayout.addWidget(self.reduceButton)
        self.amplifyButton = QtWidgets.QPushButton(ShowImageDialog)
        self.amplifyButton.setMinimumSize(QtCore.QSize(50, 50))
        self.amplifyButton.setMaximumSize(QtCore.QSize(50, 50))
        self.amplifyButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icon/amplify.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.amplifyButton.setIcon(icon2)
        self.amplifyButton.setIconSize(QtCore.QSize(40, 40))
        self.amplifyButton.setObjectName("amplifyButton")
        self.horizontalLayout.addWidget(self.amplifyButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(ShowImageDialog)
        QtCore.QMetaObject.connectSlotsByName(ShowImageDialog)

    def retranslateUi(self, ShowImageDialog):
        _translate = QtCore.QCoreApplication.translate
        ShowImageDialog.setWindowTitle(_translate("ShowImageDialog", "ShowImage"))