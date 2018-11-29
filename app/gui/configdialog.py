# -*- coding: utf-8 -*-
from PyQt4.QtGui import QComboBox, QDialog, QLabel, QLineEdit


class ConfigDialog(QDialog):
    def __init__(self, configObject, ui_dialogConfig, attributes, optionalAttributes):
        super(ConfigDialog, self).__init__()
        self.ui = ui_dialogConfig()
        self.ui.setupUi(self)

        self.configObject = configObject
        self.attributes = attributes
        self.optionalAttributes = optionalAttributes

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

    def setErrorLabel(self, text):
        self.ui.informationLabel.setText(text)

    def setGroups(self, field):
        field.addItem(str())  # add empty element on list begin
        for group in self.configObject.getGroupsList():
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

        return response

    def setInputValues(self, element, generateNewName=False):
        for attribute in self.attributes:
            field = getattr(self.ui, attribute)
            value = getattr(element, attribute, '')

            if value is None:
                value = ''

            # todo: refactor because generateNewName is in use only in hosts
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

    def add(self):
        self.ui.buttonBox.accepted.connect(lambda: self._accept("create"))
        return self._execDialog()

    def edit(self, elementName):
        element = self.configObject.get(elementName)
        self.setInputValues(element)
        self.ui.buttonBox.accepted.connect(lambda: self._accept("update", element))
        return self._execDialog()

    def _accept(self, action, element=None):
        try:
            attributesDict = self.collectFieldsValues()
            if action == "create":
                self.configObject.create(**attributesDict)
            elif action == "update":
                for key, value in attributesDict.iteritems():
                    setattr(element, key, value)
                    self.configObject._db.tryCommit()
            else:
                raise NotImplementedError("Not supported action")
        except Exception as e:
            self.setErrorLabel(e.message)
        else:
            self.accept()
