# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\liwan\Desktop\project\ui\camera.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from classdir.QtClass import ImageBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1116, 656)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/熊猫.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("QMessageBox{\n"
"    background-color: rgb(104, 104, 104);\n"
"}\n"
"QTabWidget::pane{\n"
"    border: none;\n"
"}\n"
"QLabel{\n"
"    font-size: 18px;\n"
"    font-family: \"Microsoft YaHei\";\n"
"    font-weight: bold;\n"
"     border-radius:9px;\n"
"    background:rgba(66, 195, 255, 0);\n"
"    color: rgb(218, 218, 218);\n"
"}\n"
"#sideColor, #angleColor,\n"
"#lightColor, #whiteColor,\n"
"#darkColor, #apertureColor {\n"
"    font: 150 14pt \"Agency FB\";\n"
"}\n"
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
"}        \n"
"QPushButton::disabled{font-family: \"Microsoft YaHei\";\n"
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
"    border-color: rgba(255, 255, 255, 255);\n"
"    border-radius: 3px;\n"
"    background-color:  #bf513b;\n"
"}\n"
"QPushButton::hover {\n"
"    border-style: solid;\n"
"    border-width: 0px;\n"
"    border-radius: 0px;\n"
"    background-color: rgba(48,148,243,80);\n"
"}\n"
"#queryButton {\n"
"    font-size: 24px;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cameraTabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.cameraTabWidget.setStyleSheet("#settingWidget{\n"
"background-color: rgba(95, 95, 95, 0.5);\n"
"}\n"
"#cameraWidget{\n"
"background-color: rgba(95, 95, 95, 0.5);\n"
"}")
        self.cameraTabWidget.setObjectName("cameraTabWidget")
        self.settingWidget = QtWidgets.QWidget()
        self.settingWidget.setObjectName("settingWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.settingWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 20)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        spacerItem = QtWidgets.QSpacerItem(20, 219, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.centerHorizontalLayout = QtWidgets.QHBoxLayout()
        self.centerHorizontalLayout.setObjectName("centerHorizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.centerHorizontalLayout.addItem(spacerItem1)
        self.centerVerticalLayout = QtWidgets.QVBoxLayout()
        self.centerVerticalLayout.setSpacing(0)
        self.centerVerticalLayout.setObjectName("centerVerticalLayout")
        self.topCenterHorizontalLayout = QtWidgets.QHBoxLayout()
        self.topCenterHorizontalLayout.setSpacing(0)
        self.topCenterHorizontalLayout.setObjectName("topCenterHorizontalLayout")
        self.floderLabel = QtWidgets.QLabel(self.settingWidget)
        self.floderLabel.setMinimumSize(QtCore.QSize(140, 0))
        self.floderLabel.setMaximumSize(QtCore.QSize(140, 16777215))
        self.floderLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.floderLabel.setObjectName("floderLabel")
        self.topCenterHorizontalLayout.addWidget(self.floderLabel)
        self.floderEdit = QtWidgets.QLineEdit(self.settingWidget)
        self.floderEdit.setMinimumSize(QtCore.QSize(250, 0))
        self.floderEdit.setText("")
        self.floderEdit.setObjectName("floderEdit")
        self.topCenterHorizontalLayout.addWidget(self.floderEdit)
        self.floderButton = QtWidgets.QPushButton(self.settingWidget)
        self.floderButton.setMinimumSize(QtCore.QSize(55, 28))
        self.floderButton.setMaximumSize(QtCore.QSize(16777215, 28))
        self.floderButton.setStyleSheet("QPushButton{font-family: \"Microsoft YaHei\";\n"
"font-size: 14px;\n"
"font-weight: bold;\n"
"color:white;\n"
"text-align: center center;\n"
"padding-left: 5px;\n"
"padding-right: 5px;\n"
"padding-top: 4px;\n"
"padding-bottom: 4px;\n"
"border-style: solid;\n"
"border-width: 0px;\n"
"border-color: rgba(255, 255, 255, 255);\n"
"border-radius: 3px;\n"
"background-color: rgba(200, 200, 200,0);}\n"
"\n"
"QPushButton:focus{outline: none;}\n"
"\n"
"QPushButton::pressed{font-family: \"Microsoft YaHei\";\n"
"                     font-size: 14px;\n"
"                     font-weight: bold;\n"
"                     color:rgb(200,200,200);\n"
"                     text-align: center center;\n"
"                     padding-left: 5px;\n"
"                     padding-right: 5px;\n"
"                     padding-top: 4px;\n"
"                     padding-bottom: 4px;\n"
"                     border-style: solid;\n"
"                     border-width: 0px;\n"
"                     border-color: rgba(255, 255, 255, 255);\n"
"                     border-radius: 3px;\n"
"                     background-color:  #bf513b;}\n"
"\n"
"QPushButton::disabled{font-family: \"Microsoft YaHei\";\n"
"                     font-size: 14px;\n"
"                     font-weight: bold;\n"
"                     color:rgb(200,200,200);\n"
"                     text-align: center center;\n"
"                     padding-left: 5px;\n"
"                     padding-right: 5px;\n"
"                     padding-top: 4px;\n"
"                     padding-bottom: 4px;\n"
"                     border-style: solid;\n"
"                     border-width: 0px;\n"
"                     border-color: rgba(255, 255, 255, 255);\n"
"                     border-radius: 3px;\n"
"                     background-color:  #bf513b;}\n"
"QPushButton::hover {\n"
"border-style: solid;\n"
"border-width: 0px;\n"
"border-radius: 0px;\n"
"background-color: rgba(48,148,243,80);}")
        self.floderButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icon/打开.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.floderButton.setIcon(icon1)
        self.floderButton.setObjectName("floderButton")
        self.topCenterHorizontalLayout.addWidget(self.floderButton)
        self.centerVerticalLayout.addLayout(self.topCenterHorizontalLayout)
        self.centerCenterHorizontalLayout = QtWidgets.QHBoxLayout()
        self.centerCenterHorizontalLayout.setSpacing(0)
        self.centerCenterHorizontalLayout.setObjectName("centerCenterHorizontalLayout")
        self.label = QtWidgets.QLabel(self.settingWidget)
        self.label.setMinimumSize(QtCore.QSize(140, 0))
        self.label.setMaximumSize(QtCore.QSize(140, 16777215))
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.centerCenterHorizontalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.settingWidget)
        self.comboBox.setObjectName("comboBox")
        self.centerCenterHorizontalLayout.addWidget(self.comboBox)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.centerCenterHorizontalLayout.addItem(spacerItem2)
        self.centerVerticalLayout.addLayout(self.centerCenterHorizontalLayout)
        self.bottomCenterHorizontalLayout = QtWidgets.QHBoxLayout()
        self.bottomCenterHorizontalLayout.setSpacing(0)
        self.bottomCenterHorizontalLayout.setObjectName("bottomCenterHorizontalLayout")
        self.timeLabel = QtWidgets.QLabel(self.settingWidget)
        self.timeLabel.setMinimumSize(QtCore.QSize(140, 0))
        self.timeLabel.setMaximumSize(QtCore.QSize(140, 16777215))
        self.timeLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.bottomCenterHorizontalLayout.addWidget(self.timeLabel)
        self.timeNum = QtWidgets.QSpinBox(self.settingWidget)
        self.timeNum.setMinimumSize(QtCore.QSize(60, 25))
        self.timeNum.setMaximumSize(QtCore.QSize(60, 25))
        self.timeNum.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.timeNum.setStyleSheet("QSpinBox{\n"
"background:rgba(200, 200, 200,50);\n"
"color:white;\n"
"font-size: 14px;\n"
"font-family: \"Microsoft YaHei UI\";\n"
"border-style: solid;\n"
"border-width: 1px;\n"
"border-color: rgba(200, 200, 200,100);\n"
"border-radius: 3px;}\n"
"\n"
"QSpinBox::down-button{\n"
"background:rgba(200, 200, 200,0);\n"
"border-image: url(icon/箭头_列表展开.png);}\n"
"QDoubleSpinBox::down-button::hover{\n"
"background:rgba(200, 200, 200,100);\n"
"border-image: url(icon/箭头_列表展开.png);}\n"
"\n"
"QSpinBox::up-button{\n"
"background:rgba(200, 200, 200,0);\n"
"border-image: url(icon/箭头_列表收起.png);}\n"
"QSpinBox::up-button::hover{\n"
"background:rgba(200, 200, 200,100);\n"
"border-image: url(icon/箭头_列表收起.png);}\n"
"")
        self.timeNum.setKeyboardTracking(False)
        self.timeNum.setMinimum(1)
        self.timeNum.setMaximum(600)
        self.timeNum.setSingleStep(1)
        self.timeNum.setStepType(QtWidgets.QAbstractSpinBox.DefaultStepType)
        self.timeNum.setProperty("value", 5)
        self.timeNum.setObjectName("timeNum")
        self.bottomCenterHorizontalLayout.addWidget(self.timeNum)
        self.SLabel = QtWidgets.QLabel(self.settingWidget)
        self.SLabel.setMaximumSize(QtCore.QSize(140, 16777215))
        self.SLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SLabel.setObjectName("SLabel")
        self.bottomCenterHorizontalLayout.addWidget(self.SLabel)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bottomCenterHorizontalLayout.addItem(spacerItem3)
        self.centerVerticalLayout.addLayout(self.bottomCenterHorizontalLayout)
        self.centerHorizontalLayout.addLayout(self.centerVerticalLayout)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.centerHorizontalLayout.addItem(spacerItem4)
        self.verticalLayout_3.addLayout(self.centerHorizontalLayout)
        spacerItem5 = QtWidgets.QSpacerItem(442, 13, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem5)
        spacerItem6 = QtWidgets.QSpacerItem(20, 232, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem6)
        self.BHorizontalLayout = QtWidgets.QHBoxLayout()
        self.BHorizontalLayout.setContentsMargins(-1, -1, 0, -1)
        self.BHorizontalLayout.setSpacing(100)
        self.BHorizontalLayout.setObjectName("BHorizontalLayout")
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.BHorizontalLayout.addItem(spacerItem7)
        self.enterButton = QtWidgets.QPushButton(self.settingWidget)
        self.enterButton.setObjectName("enterButton")
        self.BHorizontalLayout.addWidget(self.enterButton)
        self.cancelButton = QtWidgets.QPushButton(self.settingWidget)
        self.cancelButton.setDefault(False)
        self.cancelButton.setObjectName("cancelButton")
        self.BHorizontalLayout.addWidget(self.cancelButton)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.BHorizontalLayout.addItem(spacerItem8)
        self.verticalLayout_3.addLayout(self.BHorizontalLayout)
        self.cameraTabWidget.addTab(self.settingWidget, "")
        self.cameraWidget = QtWidgets.QWidget()
        self.cameraWidget.setObjectName("cameraWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.cameraWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.homeLeftVerticalLayout = QtWidgets.QVBoxLayout()
        self.homeLeftVerticalLayout.setSpacing(0)
        self.homeLeftVerticalLayout.setObjectName("homeLeftVerticalLayout")
        self.nameLabel = QtWidgets.QLabel(self.cameraWidget)
        self.nameLabel.setText("")
        self.nameLabel.setObjectName("nameLabel")
        self.homeLeftVerticalLayout.addWidget(self.nameLabel)
        self.homeCenterGridLayout = QtWidgets.QGridLayout()
        self.homeCenterGridLayout.setHorizontalSpacing(10)
        self.homeCenterGridLayout.setVerticalSpacing(0)
        self.homeCenterGridLayout.setObjectName("homeCenterGridLayout")
        self.ANSLabel = QtWidgets.QLabel(self.cameraWidget)
        self.ANSLabel.setMaximumSize(QtCore.QSize(16777215, 30))
        self.ANSLabel.setStyleSheet("font: 16pt \"Agency FB\";")
        self.ANSLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ANSLabel.setObjectName("ANSLabel")
        self.homeCenterGridLayout.addWidget(self.ANSLabel, 0, 0, 1, 1)
        self.ODLabel = QtWidgets.QLabel(self.cameraWidget)
        self.ODLabel.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.ODLabel.setStyleSheet("font: 16pt \"Agency FB\";")
        self.ODLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.ODLabel.setObjectName("ODLabel")
        self.homeCenterGridLayout.addWidget(self.ODLabel, 0, 1, 1, 1)
        self.inputImage = ImageBox(self.cameraWidget)
        self.inputImage.setStyleSheet("QGraphicsView{\n"
"background-color: rgba(75, 75, 75, 0.5);\n"
"border: 0px solid #42adff;\n"
"border-radius:0px;}")
        self.inputImage.setObjectName("inputImage")
        self.homeCenterGridLayout.addWidget(self.inputImage, 1, 0, 1, 1)
        self.outImage = ImageBox(self.cameraWidget)
        self.outImage.setStyleSheet("QGraphicsView{\n"
"background-color: rgba(75, 75, 75, 0.5);\n"
"border: 0px solid #42adff;\n"
"border-radius:0px;\n"
"}")
        self.outImage.setObjectName("outImage")
        self.homeCenterGridLayout.addWidget(self.outImage, 1, 1, 1, 1)
        self.homeLeftVerticalLayout.addLayout(self.homeCenterGridLayout)
        self.homeEndHorizontalLayout = QtWidgets.QHBoxLayout()
        self.homeEndHorizontalLayout.setObjectName("homeEndHorizontalLayout")
        self.homeEndLeftFormLayout = QtWidgets.QFormLayout()
        self.homeEndLeftFormLayout.setContentsMargins(10, 10, 10, 10)
        self.homeEndLeftFormLayout.setVerticalSpacing(0)
        self.homeEndLeftFormLayout.setObjectName("homeEndLeftFormLayout")
        self.currentLabel = QtWidgets.QLabel(self.cameraWidget)
        self.currentLabel.setStyleSheet("font: 14pt \"Agency FB\";")
        self.currentLabel.setObjectName("currentLabel")
        self.homeEndLeftFormLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.currentLabel)
        self.currentNum = QtWidgets.QLabel(self.cameraWidget)
        self.currentNum.setStyleSheet("font: 12pt \"Arial\";")
        self.currentNum.setObjectName("currentNum")
        self.homeEndLeftFormLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.currentNum)
        self.flawNum = QtWidgets.QLabel(self.cameraWidget)
        self.flawNum.setStyleSheet("font: 12pt \"Arial\";")
        self.flawNum.setObjectName("flawNum")
        self.homeEndLeftFormLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.flawNum)
        self.standLabel = QtWidgets.QLabel(self.cameraWidget)
        self.standLabel.setStyleSheet("font: 14pt \"Agency FB\";")
        self.standLabel.setObjectName("standLabel")
        self.homeEndLeftFormLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.standLabel)
        self.standNum = QtWidgets.QLabel(self.cameraWidget)
        self.standNum.setStyleSheet("font: 12pt \"Arial\";")
        self.standNum.setObjectName("standNum")
        self.homeEndLeftFormLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.standNum)
        self.flawLabel = QtWidgets.QLabel(self.cameraWidget)
        self.flawLabel.setStyleSheet("font: 14pt \"Agency FB\";")
        self.flawLabel.setObjectName("flawLabel")
        self.homeEndLeftFormLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.flawLabel)
        self.homeEndHorizontalLayout.addLayout(self.homeEndLeftFormLayout)
        self.homeEndRightGridLayout = QtWidgets.QGridLayout()
        self.homeEndRightGridLayout.setVerticalSpacing(0)
        self.homeEndRightGridLayout.setObjectName("homeEndRightGridLayout")
        self.angleColor = QtWidgets.QLabel(self.cameraWidget)
        self.angleColor.setStyleSheet("")
        self.angleColor.setObjectName("angleColor")
        self.homeEndRightGridLayout.addWidget(self.angleColor, 1, 2, 1, 1)
        self.lightLabel = QtWidgets.QLabel(self.cameraWidget)
        self.lightLabel.setStyleSheet("font: 14pt \"Agency FB\";")
        self.lightLabel.setObjectName("lightLabel")
        self.homeEndRightGridLayout.addWidget(self.lightLabel, 3, 0, 1, 1)
        self.sideColor = QtWidgets.QLabel(self.cameraWidget)
        self.sideColor.setStyleSheet("")
        self.sideColor.setObjectName("sideColor")
        self.homeEndRightGridLayout.addWidget(self.sideColor, 0, 2, 1, 1)
        self.angleNum = QtWidgets.QLabel(self.cameraWidget)
        self.angleNum.setStyleSheet("font: 12pt \"Arial\";")
        self.angleNum.setObjectName("angleNum")
        self.homeEndRightGridLayout.addWidget(self.angleNum, 1, 1, 1, 1)
        self.darkNum = QtWidgets.QLabel(self.cameraWidget)
        self.darkNum.setStyleSheet("font: 12pt \"Arial\";")
        self.darkNum.setObjectName("darkNum")
        self.homeEndRightGridLayout.addWidget(self.darkNum, 4, 1, 1, 1)
        self.apertureLabel = QtWidgets.QLabel(self.cameraWidget)
        self.apertureLabel.setStyleSheet("font: 14pt \"Agency FB\";")
        self.apertureLabel.setObjectName("apertureLabel")
        self.homeEndRightGridLayout.addWidget(self.apertureLabel, 5, 0, 1, 1)
        self.whiteLabel = QtWidgets.QLabel(self.cameraWidget)
        self.whiteLabel.setStyleSheet("font: 14pt \"Agency FB\";")
        self.whiteLabel.setObjectName("whiteLabel")
        self.homeEndRightGridLayout.addWidget(self.whiteLabel, 2, 0, 1, 1)
        self.whiteNum = QtWidgets.QLabel(self.cameraWidget)
        self.whiteNum.setStyleSheet("font: 12pt \"Arial\";")
        self.whiteNum.setObjectName("whiteNum")
        self.homeEndRightGridLayout.addWidget(self.whiteNum, 2, 1, 1, 1)
        self.sideLabel = QtWidgets.QLabel(self.cameraWidget)
        self.sideLabel.setStyleSheet("font: 14pt \"Agency FB\";")
        self.sideLabel.setObjectName("sideLabel")
        self.homeEndRightGridLayout.addWidget(self.sideLabel, 0, 0, 1, 1)
        self.lightNum = QtWidgets.QLabel(self.cameraWidget)
        self.lightNum.setStyleSheet("font: 12pt \"Arial\";")
        self.lightNum.setObjectName("lightNum")
        self.homeEndRightGridLayout.addWidget(self.lightNum, 3, 1, 1, 1)
        self.angleLabel = QtWidgets.QLabel(self.cameraWidget)
        self.angleLabel.setStyleSheet("font: 14pt \"Agency FB\";")
        self.angleLabel.setObjectName("angleLabel")
        self.homeEndRightGridLayout.addWidget(self.angleLabel, 1, 0, 1, 1)
        self.apertureNum = QtWidgets.QLabel(self.cameraWidget)
        self.apertureNum.setStyleSheet("font: 12pt \"Arial\";")
        self.apertureNum.setObjectName("apertureNum")
        self.homeEndRightGridLayout.addWidget(self.apertureNum, 5, 1, 1, 1)
        self.sideNum = QtWidgets.QLabel(self.cameraWidget)
        self.sideNum.setStyleSheet("font: 12pt \"Arial\";")
        self.sideNum.setObjectName("sideNum")
        self.homeEndRightGridLayout.addWidget(self.sideNum, 0, 1, 1, 1)
        self.whiteColor = QtWidgets.QLabel(self.cameraWidget)
        self.whiteColor.setStyleSheet("")
        self.whiteColor.setObjectName("whiteColor")
        self.homeEndRightGridLayout.addWidget(self.whiteColor, 2, 2, 1, 1)
        self.darkLabel = QtWidgets.QLabel(self.cameraWidget)
        self.darkLabel.setStyleSheet("font: 14pt \"Agency FB\";")
        self.darkLabel.setObjectName("darkLabel")
        self.homeEndRightGridLayout.addWidget(self.darkLabel, 4, 0, 1, 1)
        self.lightColor = QtWidgets.QLabel(self.cameraWidget)
        self.lightColor.setStyleSheet("")
        self.lightColor.setObjectName("lightColor")
        self.homeEndRightGridLayout.addWidget(self.lightColor, 3, 2, 1, 1)
        self.darkColor = QtWidgets.QLabel(self.cameraWidget)
        self.darkColor.setStyleSheet("")
        self.darkColor.setObjectName("darkColor")
        self.homeEndRightGridLayout.addWidget(self.darkColor, 4, 2, 1, 1)
        self.apertureColor = QtWidgets.QLabel(self.cameraWidget)
        self.apertureColor.setStyleSheet("")
        self.apertureColor.setObjectName("apertureColor")
        self.homeEndRightGridLayout.addWidget(self.apertureColor, 5, 2, 1, 1)
        self.homeEndHorizontalLayout.addLayout(self.homeEndRightGridLayout)
        self.homeLeftVerticalLayout.addLayout(self.homeEndHorizontalLayout)
        self.horizontalLayout_2.addLayout(self.homeLeftVerticalLayout)
        self.horizontalLayout_2.setStretch(0, 10)
        self.cameraTabWidget.addTab(self.cameraWidget, "")
        self.verticalLayout.addWidget(self.cameraTabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.cameraTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "CameraWindow"))
        self.floderLabel.setText(_translate("MainWindow", "图像存放目录："))
        self.floderButton.setToolTip(_translate("MainWindow", "file"))
        self.label.setText(_translate("MainWindow", "摄像头编号："))
        self.timeLabel.setText(_translate("MainWindow", "拍摄间隔："))
        self.SLabel.setText(_translate("MainWindow", "s"))
        self.enterButton.setText(_translate("MainWindow", "ok"))
        self.cancelButton.setText(_translate("MainWindow", "Cancel"))
        self.cameraTabWidget.setTabText(self.cameraTabWidget.indexOf(self.settingWidget), _translate("MainWindow", "setting"))
        self.ANSLabel.setText(_translate("MainWindow", "原图"))
        self.ODLabel.setText(_translate("MainWindow", "结果图"))
        self.currentLabel.setText(_translate("MainWindow", "当前已读图像数量："))
        self.currentNum.setText(_translate("MainWindow", "0"))
        self.flawNum.setText(_translate("MainWindow", "0"))
        self.standLabel.setText(_translate("MainWindow", "标准瓷砖总数目："))
        self.standNum.setText(_translate("MainWindow", "0"))
        self.flawLabel.setText(_translate("MainWindow", "瑕疵瓷砖总数目："))
        self.angleColor.setText(_translate("MainWindow", "■"))
        self.lightLabel.setText(_translate("MainWindow", "浅色块瑕疵数目："))
        self.sideColor.setText(_translate("MainWindow", "■"))
        self.angleNum.setText(_translate("MainWindow", "0"))
        self.darkNum.setText(_translate("MainWindow", "0"))
        self.apertureLabel.setText(_translate("MainWindow", "光圈瑕疵数目："))
        self.whiteLabel.setText(_translate("MainWindow", "白色点瑕疵数目："))
        self.whiteNum.setText(_translate("MainWindow", "0"))
        self.sideLabel.setText(_translate("MainWindow", "边异常数目："))
        self.lightNum.setText(_translate("MainWindow", "0"))
        self.angleLabel.setText(_translate("MainWindow", "角异常数目："))
        self.apertureNum.setText(_translate("MainWindow", "0"))
        self.sideNum.setText(_translate("MainWindow", "0"))
        self.whiteColor.setText(_translate("MainWindow", "■"))
        self.darkLabel.setText(_translate("MainWindow", "深色点块瑕疵数目："))
        self.lightColor.setText(_translate("MainWindow", "■"))
        self.darkColor.setText(_translate("MainWindow", "■"))
        self.apertureColor.setText(_translate("MainWindow", "■"))
        self.cameraTabWidget.setTabText(self.cameraTabWidget.indexOf(self.cameraWidget), _translate("MainWindow", "camera"))
