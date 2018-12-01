# -*- coding: utf-8 -*-
from app.gui.configdialog import ConfigDialog
from PyQt4.QtGui import QComboBox, QDialog, QLabel, QLineEdit
from app.gui.hostconfig_ui import Ui_HostConfig


class HostConfigDialog(ConfigDialog):
    def __init__(self, hosts):
        optionalAttributes = ['user', 'password', 'group']
        attributes = ['name', 'address'] + optionalAttributes
        super(HostConfigDialog, self).__init__(hosts, Ui_HostConfig,
                                               attributes, optionalAttributes)

        self.ui.showPassword.clicked.connect(self.changePasswordVisibility)
        self.ui.group.lineEdit().setPlaceholderText("Group")  # not available from designer
        self.hosts = hosts

    def changePasswordVisibility(self):
        if self.ui.showPassword.isChecked():
            self.ui.password.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.password.setEchoMode(QLineEdit.Password)

    def _execDialog(self):
        """
        :return: dictionary {
            "code": return code,
            "name": host name if host should be connected
            }
        """
        response = super(HostConfigDialog, self)._execDialog()

        if response.get('retCode') and self.ui.connectCheckBox.isChecked():
            response["name"] = self.ui.name.text()
        return response

    def add(self):
        self.ui.buttonBox.accepted.connect(lambda: self._accept("create"))
        self.setGroups(self.ui.group)
        return self._execDialog()

    def duplicate(self, hostName):
        host = self.hosts.get(hostName)
        self.setInputValues(host, generateNewName=True)
        return self.add()

    def setGroups(self, field):
        field.addItem(str())  # add empty element on list begin
        for group in self.configObject.getGroupsList():
            field.addItem(group)

    def setInputValues(self, values, generateNewName=False):
        for attribute in self.attributes:
            field = getattr(self.ui, attribute)
            value = values.get(attribute)

            if value is None:
                value = ''

            if generateNewName and attribute == "name":
                allNames = self.configObject.getAllHostsNames()
                suffix = 0
                newName = value
                while newName in allNames:
                    newName = u"{}_{}".format(value, suffix)
                    suffix += 1
                value = newName

            if attribute == "group":
                self.setGroups(field)
                field.lineEdit().setText(value)
            else:
                field.setText(value)
