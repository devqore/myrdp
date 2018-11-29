# -*- coding: utf-8 -*-
from app.gui.configdialog import ConfigDialog
from app.gui.groupconfig_ui import Ui_GroupConfig
from PyQt4.QtGui import QLineEdit


class GroupConfigDialog(ConfigDialog):
    def __init__(self, configObject):
        optionalAttributes = ['default_user_name', 'default_password']
        attributes = ['name'] + optionalAttributes
        super(GroupConfigDialog, self).__init__(configObject, Ui_GroupConfig,
                                                attributes, optionalAttributes)
        self.ui.showPassword.clicked.connect(self.changePasswordVisibility)

    def changePasswordVisibility(self):
        if self.ui.showPassword.isChecked():
            self.ui.default_password.setEchoMode(QLineEdit.Normal)
        else:
            self.ui.default_password.setEchoMode(QLineEdit.Password)
