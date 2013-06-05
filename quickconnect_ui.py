# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'quickconnect.ui'
#
# Created: Sun Jun  2 20:53:07 2013
#      by: PyQt4 UI code generator 4.10.1
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

class Ui_QuickConnectDialog(object):
    def setupUi(self, QuickConnectDialog):
        QuickConnectDialog.setObjectName(_fromUtf8("QuickConnectDialog"))
        QuickConnectDialog.resize(400, 172)
        self.verticalLayout = QtGui.QVBoxLayout(QuickConnectDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(QuickConnectDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.host = QtGui.QLineEdit(QuickConnectDialog)
        self.host.setObjectName(_fromUtf8("host"))
        self.gridLayout.addWidget(self.host, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(QuickConnectDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.user = QtGui.QLineEdit(QuickConnectDialog)
        self.user.setObjectName(_fromUtf8("user"))
        self.gridLayout.addWidget(self.user, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(QuickConnectDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.password = QtGui.QLineEdit(QuickConnectDialog)
        self.password.setObjectName(_fromUtf8("password"))
        self.gridLayout.addWidget(self.password, 2, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(QuickConnectDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(QuickConnectDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QuickConnectDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QuickConnectDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(QuickConnectDialog)

    def retranslateUi(self, QuickConnectDialog):
        QuickConnectDialog.setWindowTitle(_translate("QuickConnectDialog", "Quick connect", None))
        self.label.setText(_translate("QuickConnectDialog", "host", None))
        self.label_2.setText(_translate("QuickConnectDialog", "user", None))
        self.label_3.setText(_translate("QuickConnectDialog", "password", None))

