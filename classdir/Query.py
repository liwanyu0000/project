# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\ui\queryUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow


class Ui_QueryUI(QMainWindow):
    def setupUi(self, QueryUI):
        QueryUI.setObjectName("QueryUI")
        QueryUI.resize(1199, 701)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icon/熊猫.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        QueryUI.setWindowIcon(icon)
        QueryUI.setStyleSheet("QLabel\n"
"{\n"
"    font-size: 16px;\n"
"    font-family: \"Microsoft YaHei\";\n"
"    font-weight: light;\n"
"         border-radius:9px;\n"
"        background:rgba(66, 195, 255, 0);\n"
"color: rgb(218, 218, 218);\n"
"}")
        self.centralwidget = QtWidgets.QWidget(QueryUI)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setStyleSheet("#groupBox{\n"
"background-color: rgba(75, 75, 75, 200);\n"
"border: 0px solid #42adff;\n"
"border-radius:0px;}\n"
"")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(30, -1, -1, -1)
        self.horizontalLayout.setSpacing(15)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startTimeLabel = QtWidgets.QLabel(self.groupBox)
        self.startTimeLabel.setObjectName("startTimeLabel")
        self.horizontalLayout.addWidget(self.startTimeLabel)
        self.startTime = QtWidgets.QDateTimeEdit(self.groupBox)
        self.startTime.setObjectName("startTime")
        self.horizontalLayout.addWidget(self.startTime)
        self.endTimeLabel = QtWidgets.QLabel(self.groupBox)
        self.endTimeLabel.setObjectName("endTimeLabel")
        self.horizontalLayout.addWidget(self.endTimeLabel)
        self.endTime = QtWidgets.QDateTimeEdit(self.groupBox)
        self.endTime.setObjectName("endTime")
        self.horizontalLayout.addWidget(self.endTime)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.queryButton = QtWidgets.QPushButton(self.groupBox)
        self.queryButton.setObjectName("queryButton")
        self.horizontalLayout.addWidget(self.queryButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.tableList = QtWidgets.QTableWidget(self.groupBox)
        self.tableList.setStyleSheet("QTableWidget{\n"
"border: 0px solid #42adff;\n"
"border-left: 1px solid rgba(200, 200, 200,100);\n"
"border-right: 0px solid rgba(29, 83, 185, 255);\n"
"border-radius:0px;}")
        self.tableList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableList.setAlternatingRowColors(True)
        self.tableList.setObjectName("tableList")
        self.tableList.setColumnCount(3)
        self.tableList.setRowCount(5)
        item = QtWidgets.QTableWidgetItem()
        self.tableList.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableList.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableList.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableList.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableList.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableList.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableList.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableList.setHorizontalHeaderItem(2, item)
        self.tableList.horizontalHeader().setVisible(True)
        self.tableList.horizontalHeader().setCascadingSectionResizes(False)
        self.tableList.horizontalHeader().setDefaultSectionSize(220)
        self.tableList.horizontalHeader().setHighlightSections(True)
        self.tableList.horizontalHeader().setStretchLastSection(True)
        self.tableList.verticalHeader().setVisible(True)
        self.tableList.verticalHeader().setDefaultSectionSize(44)
        self.tableList.verticalHeader().setMinimumSectionSize(28)
        self.tableList.verticalHeader().setSortIndicatorShown(False)
        self.tableList.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.tableList)
        self.verticalLayout_2.addWidget(self.groupBox)
        QueryUI.setCentralWidget(self.centralwidget)

        self.retranslateUi(QueryUI)
        QtCore.QMetaObject.connectSlotsByName(QueryUI)

    def retranslateUi(self, QueryUI):
        _translate = QtCore.QCoreApplication.translate
        QueryUI.setWindowTitle(_translate("QueryUI", "结果查询"))
        self.startTimeLabel.setText(_translate("QueryUI", "开始时间"))
        self.endTimeLabel.setText(_translate("QueryUI", "结束时间"))
        self.queryButton.setText(_translate("QueryUI", "查询"))
        item = self.tableList.verticalHeaderItem(0)
        item.setText(_translate("QueryUI", "1"))
        item = self.tableList.verticalHeaderItem(1)
        item.setText(_translate("QueryUI", "2"))
        item = self.tableList.verticalHeaderItem(2)
        item.setText(_translate("QueryUI", "3"))
        item = self.tableList.verticalHeaderItem(3)
        item.setText(_translate("QueryUI", "4"))
        item = self.tableList.verticalHeaderItem(4)
        item.setText(_translate("QueryUI", "5"))
        item = self.tableList.horizontalHeaderItem(0)
        item.setText(_translate("QueryUI", "文件名"))
        item = self.tableList.horizontalHeaderItem(1)
        item.setText(_translate("QueryUI", "瑕疵总数"))
        item = self.tableList.horizontalHeaderItem(2)
        item.setText(_translate("QueryUI", "日期"))
# import apprcc_rc