# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/hostconfig.ui'
#
# Created by: PyQt5 UI code generator 5.4.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_HostConfig(object):
    def setupUi(self, HostConfig):
        HostConfig.setObjectName("HostConfig")
        HostConfig.resize(270, 198)
        self.verticalLayout = QtWidgets.QVBoxLayout(HostConfig)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name = QtWidgets.QLineEdit(HostConfig)
        self.name.setText("")
        self.name.setObjectName("name")
        self.verticalLayout.addWidget(self.name)
        self.address = QtWidgets.QLineEdit(HostConfig)
        self.address.setObjectName("address")
        self.verticalLayout.addWidget(self.address)
        self.user = QtWidgets.QLineEdit(HostConfig)
        self.user.setObjectName("user")
        self.verticalLayout.addWidget(self.user)
        self.password = QtWidgets.QLineEdit(HostConfig)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")
        self.verticalLayout.addWidget(self.password)
        self.errorArea = QtWidgets.QVBoxLayout()
        self.errorArea.setObjectName("errorArea")
        self.verticalLayout.addLayout(self.errorArea)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.connectCheckBox = QtWidgets.QCheckBox(HostConfig)
        self.connectCheckBox.setEnabled(False)
        self.connectCheckBox.setChecked(True)
        self.connectCheckBox.setObjectName("connectCheckBox")
        self.horizontalLayout.addWidget(self.connectCheckBox)
        self.saveCheckBox = QtWidgets.QCheckBox(HostConfig)
        self.saveCheckBox.setEnabled(False)
        self.saveCheckBox.setChecked(True)
        self.saveCheckBox.setObjectName("saveCheckBox")
        self.horizontalLayout.addWidget(self.saveCheckBox)
        self.acceptButton = QtWidgets.QPushButton(HostConfig)
        self.acceptButton.setObjectName("acceptButton")
        self.horizontalLayout.addWidget(self.acceptButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(HostConfig)
        QtCore.QMetaObject.connectSlotsByName(HostConfig)

    def retranslateUi(self, HostConfig):
        _translate = QtCore.QCoreApplication.translate
        HostConfig.setWindowTitle(_translate("HostConfig", "Form"))
        self.name.setPlaceholderText(_translate("HostConfig", "Name"))
        self.address.setPlaceholderText(_translate("HostConfig", "Host"))
        self.user.setPlaceholderText(_translate("HostConfig", "User"))
        self.password.setPlaceholderText(_translate("HostConfig", "Password"))
        self.connectCheckBox.setText(_translate("HostConfig", "connect"))
        self.saveCheckBox.setText(_translate("HostConfig", "save"))
        self.acceptButton.setText(_translate("HostConfig", "Accept"))

