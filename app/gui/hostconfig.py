# -*- coding: utf-8 -*-
from PyQt4.QtGui import QComboBox, QDialog, QLabel, QLineEdit
from app.gui.hostconfig_ui import Ui_HostConfig


class HostConfigDialog(QDialog):
    def __init__(self, hosts):
        super(HostConfigDialog, self).__init__()
        self.ui = Ui_HostConfig()
        self.ui.setupUi(self)
        self.ui.showPassword.clicked.connect(self.changePasswordVisibility)
        self.ui.group.lineEdit().setPlaceholderText("Group")  # not available from designer
        self.hosts = hosts

        self.optionalAttributes = ['user', 'password', 'group']
        self.attributes = ['name', 'address'] + self.optionalAttributes

    def changePasswordVisibility(self):
        if self.ui.showPassword.isChecked():
            self.ui.password.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.password.setEchoMode(QLineEdit.Password)

    def getTextFieldValue(self, field):
        """ field value or None
        :param field: object id
        :return: value or None
        """
        fieldObject = getattr(self.ui, field)
        if not isinstance(fieldObject, QComboBox):
            value = fieldObject.text()
        else:
            value = fieldObject.lineEdit().text()
        if value == '':
            if field not in self.optionalAttributes:
                raise ValueError(u"Complete the required fields")
            return None
        return unicode(value)

    def collectFieldsValues(self):
        attributesDict = {}
        for attr in self.attributes:
            attributesDict[attr] = self.getTextFieldValue(attr)
        return attributesDict

    def _accept(self, action, host=None):
        try:
            attributesDict = self.collectFieldsValues()
            if action == "create":
                self.hosts.create(**attributesDict)
            elif action == "update":
                self.hosts.updateHostValues(host, attributesDict)
            else:
                raise NotImplementedError("Not supported action")
        except Exception as e:
            self.setErrorLabel(e.message)
        else:
            self.accept()

    def setErrorLabel(self, text):
        self.ui.informationLabel.setText(text)

    def setGroups(self, field):
        field.addItem(str())  # add empty element on list begin
        for group in self.hosts.getGroupsList():
            field.addItem(group)

    def _execDialog(self):
        """
        :return: dictionary {
            "code": return code,
            "name": host name if host should be connected
            }
        """
        response = dict()
        retCode = self.exec_()
        response["code"] = retCode

        if retCode and self.ui.connectCheckBox.isChecked():
            response["name"] = self.ui.name.text()
        return response

    def setInputValues(self, host, generateNewName=False):
        for attribute in self.attributes:
            field = getattr(self.ui, attribute)
            value = getattr(host, attribute, '')

            if value is None:
                value = ''

            if generateNewName and attribute == "name":
                allNames = self.hosts.getAllHostsNames()
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

    def add(self):
        self.ui.buttonBox.accepted.connect(lambda: self._accept("create"))
        self.setGroups(self.ui.group)
        return self._execDialog()

    def edit(self, hostName):
        host = self.hosts.get(hostName)
        self.setInputValues(host)
        self.ui.buttonBox.accepted.connect(lambda: self._accept("update", host))
        return self._execDialog()

    def duplicate(self, hostName):
        host = self.hosts.get(hostName)
        self.setInputValues(host, generateNewName=True)
        return self.add()