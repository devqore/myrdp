# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(819, 584)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/ico/myrdp.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        MainWindow.setCentralWidget(self.centralWidget)
        self.hostsDock = QtWidgets.QDockWidget(MainWindow)
        self.hostsDock.setAutoFillBackground(True)
        self.hostsDock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable|QtWidgets.QDockWidget.DockWidgetMovable)
        self.hostsDock.setObjectName("hostsDock")
        self.hostsWidget = QtWidgets.QWidget()
        self.hostsWidget.setObjectName("hostsWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.hostsWidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.addHost = QtWidgets.QPushButton(self.hostsWidget)
        self.addHost.setObjectName("addHost")
        self.verticalLayout_3.addWidget(self.addHost)
        self.hostsList = QtWidgets.QListWidget(self.hostsWidget)
        self.hostsList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.hostsList.setAutoFillBackground(True)
        self.hostsList.setAlternatingRowColors(True)
        self.hostsList.setWordWrap(True)
        self.hostsList.setObjectName("hostsList")
        self.verticalLayout_3.addWidget(self.hostsList)
        self.hostsDock.setWidget(self.hostsWidget)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.hostsDock)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MyRDP"))
        self.hostsDock.setWindowTitle(_translate("MainWindow", "Hosts &lists"))
        self.addHost.setText(_translate("MainWindow", "Add host"))
        self.hostsList.setSortingEnabled(True)

import resources_rc
