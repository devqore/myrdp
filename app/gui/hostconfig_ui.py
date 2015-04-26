# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/hostconfig.ui'
#
# Created: Sun Apr 26 09:08:32 2015
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

class Ui_HostConfig(object):
    def setupUi(self, HostConfig):
        HostConfig.setObjectName(_fromUtf8("HostConfig"))
        HostConfig.resize(270, 198)
        self.verticalLayout = QtGui.QVBoxLayout(HostConfig)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.name = QtGui.QLineEdit(HostConfig)
        self.name.setText(_fromUtf8(""))
        self.name.setObjectName(_fromUtf8("name"))
        self.verticalLayout.addWidget(self.name)
        self.address = QtGui.QLineEdit(HostConfig)
        self.address.setObjectName(_fromUtf8("address"))
        self.verticalLayout.addWidget(self.address)
        self.user = QtGui.QLineEdit(HostConfig)
        self.user.setObjectName(_fromUtf8("user"))
        self.verticalLayout.addWidget(self.user)
        self.password = QtGui.QLineEdit(HostConfig)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.verticalLayout.addWidget(self.password)
        self.errorArea = QtGui.QVBoxLayout()
        self.errorArea.setObjectName(_fromUtf8("errorArea"))
        self.verticalLayout.addLayout(self.errorArea)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.connectCheckBox = QtGui.QCheckBox(HostConfig)
        self.connectCheckBox.setEnabled(True)
        self.connectCheckBox.setChecked(True)
        self.connectCheckBox.setObjectName(_fromUtf8("connectCheckBox"))
        self.horizontalLayout.addWidget(self.connectCheckBox)
        self.acceptButton = QtGui.QPushButton(HostConfig)
        self.acceptButton.setObjectName(_fromUtf8("acceptButton"))
        self.horizontalLayout.addWidget(self.acceptButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(HostConfig)
        QtCore.QMetaObject.connectSlotsByName(HostConfig)

    def retranslateUi(self, HostConfig):
        HostConfig.setWindowTitle(_translate("HostConfig", "Host config", None))
        self.name.setPlaceholderText(_translate("HostConfig", "Name", None))
        self.address.setPlaceholderText(_translate("HostConfig", "Host", None))
        self.user.setPlaceholderText(_translate("HostConfig", "User", None))
        self.password.setPlaceholderText(_translate("HostConfig", "Password", None))
        self.connectCheckBox.setText(_translate("HostConfig", "connect", None))
        self.acceptButton.setText(_translate("HostConfig", "Accept", None))

