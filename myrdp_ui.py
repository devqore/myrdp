# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myrdp.ui'
#
# Created: Thu Jan 31 20:09:40 2013
#      by: PyQt4 UI code generator 4.9.6
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
#         MainWindow.setFocusPolicy(QtCore.Qt.NoFocus)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/ico/ico/myrdp.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralWidget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        MainWindow.setCentralWidget(self.centralWidget)
        self.hostsDock = QtGui.QDockWidget(MainWindow)
        self.hostsDock.setAutoFillBackground(True)
        self.hostsDock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable|QtGui.QDockWidget.DockWidgetClosable)
        self.hostsDock.setObjectName(_fromUtf8("hostsDock"))
        self.hostsWidget = QtGui.QWidget()
        self.hostsWidget.setObjectName(_fromUtf8("hostsWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.hostsWidget)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.menu = QtGui.QPushButton(self.hostsWidget)
#         self.menu.setFocusPolicy(QtCore.Qt.NoFocus)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.verticalLayout_3.addWidget(self.menu)
        self.hostsList = QtGui.QListWidget(self.hostsWidget)
#         self.hostsList.setFocusPolicy(QtCore.Qt.NoFocus)
        self.hostsList.setAutoFillBackground(True)
        self.hostsList.setAlternatingRowColors(True)
        self.hostsList.setWordWrap(True)
        self.hostsList.setObjectName(_fromUtf8("hostsList"))
        self.verticalLayout_3.addWidget(self.hostsList)
        self.hostsDock.setWidget(self.hostsWidget)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.hostsDock)
        self.optionsDock = QtGui.QDockWidget(MainWindow)
        self.optionsDock.setObjectName(_fromUtf8("optionsDock"))
        self.optionsWidget = QtGui.QWidget()
        self.optionsWidget.setObjectName(_fromUtf8("optionsWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.optionsWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.optionsTable = QtGui.QTableWidget(self.optionsWidget)
        self.optionsTable.setObjectName(_fromUtf8("optionsTable"))
        self.optionsTable.setColumnCount(0)
        self.optionsTable.setRowCount(0)
        self.verticalLayout.addWidget(self.optionsTable)
        self.optionsDock.setWidget(self.optionsWidget)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.optionsDock)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MyRDP", None))
        self.hostsDock.setWindowTitle(_translate("MainWindow", "Hosts lists", None))
        self.menu.setText(_translate("MainWindow", "Menu", None))
        self.hostsList.setSortingEnabled(True)
        self.optionsDock.setWindowTitle(_translate("MainWindow", "options", None))

import resources_rc
