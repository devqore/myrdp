# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/hostconfig.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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
        HostConfig.resize(288, 198)
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
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.password = QtGui.QLineEdit(HostConfig)
        self.password.setEchoMode(QtGui.QLineEdit.Password)
        self.password.setObjectName(_fromUtf8("password"))
        self.horizontalLayout_2.addWidget(self.password)
        self.showPassword = QtGui.QPushButton(HostConfig)
        self.showPassword.setMaximumSize(QtCore.QSize(30, 26))
        self.showPassword.setFocusPolicy(QtCore.Qt.NoFocus)
        self.showPassword.setToolTip(_fromUtf8(""))
        self.showPassword.setAccessibleName(_fromUtf8(""))
        self.showPassword.setAccessibleDescription(_fromUtf8(""))
        self.showPassword.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/ico/eye.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.showPassword.setIcon(icon)
        self.showPassword.setIconSize(QtCore.QSize(30, 20))
        self.showPassword.setCheckable(True)
        self.showPassword.setFlat(True)
        self.showPassword.setObjectName(_fromUtf8("showPassword"))
        self.horizontalLayout_2.addWidget(self.showPassword)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/ico/ok.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.acceptButton.setIcon(icon1)
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

import resources_rc
