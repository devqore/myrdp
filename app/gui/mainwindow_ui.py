# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/mainwindow.ui'
#
# Created: Sat Mar 28 13:54:13 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(819, 584)
        MainWindow.setFocusPolicy(QtCore.Qt.StrongFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/ico/myrdp.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        MainWindow.setCentralWidget(self.centralWidget)
        self.hostsDock = QtGui.QDockWidget(MainWindow)
        self.hostsDock.setAutoFillBackground(True)
        self.hostsDock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.hostsDock.setObjectName(_fromUtf8("hostsDock"))
        self.hostsWidget = QtGui.QWidget()
        self.hostsWidget.setObjectName(_fromUtf8("hostsWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.hostsWidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.addHost = QtGui.QPushButton(self.hostsWidget)
        self.addHost.setObjectName(_fromUtf8("addHost"))
        self.verticalLayout_3.addWidget(self.addHost)
        self.hostsList = QtGui.QListWidget(self.hostsWidget)
        self.hostsList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.hostsList.setAutoFillBackground(True)
        self.hostsList.setAlternatingRowColors(True)
        self.hostsList.setWordWrap(True)
        self.hostsList.setObjectName(_fromUtf8("hostsList"))
        self.verticalLayout_3.addWidget(self.hostsList)
        self.hostsDock.setWidget(self.hostsWidget)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.hostsDock)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MyRDP", None))
        self.hostsDock.setWindowTitle(_translate("MainWindow", "Hosts &lists", None))
        self.addHost.setText(_translate("MainWindow", "Add host", None))
        self.hostsList.setSortingEnabled(True)

import resources_rc
