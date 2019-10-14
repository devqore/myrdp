# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4.QtGui import QDialog
from app.gui.setkeypassword_ui import Ui_SetKeyPasswordDialog

from app.config import Config
from app.log import logger


class SetKeyPassword(QDialog):
    def __init__(self):
        super(SetKeyPassword, self).__init__()
        self.ui = Ui_SetKeyPasswordDialog()
        self.ui.setupUi(self)

    def accept(self):
        try:
            self.savePassword()
        except Exception as e:
            self.ui.informationLabel.setText(e.message)
            return
        else:
            super(SetKeyPassword, self).accept()

    @staticmethod
    def isFieldEmpty(field):
        if field == QtCore.QString(''):
            return True
        return False

    def savePassword(self):
        currentPassword = self.ui.currentPassword.text()
        newPassword = self.ui.newPassword.text()
        repeatNewPassword = self.ui.repeatPassword.text()

        if self.isFieldEmpty(currentPassword) and self.isFieldEmpty(newPassword) and \
                self.isFieldEmpty(repeatNewPassword):
            raise ValueError("No master password changes detected")

        if newPassword != repeatNewPassword:
            raise ValueError("Passwords mismatch")

        config = Config()

        ck = config.get_private_key(str(currentPassword))
        ck.save(config.private_key_path, str(newPassword))
        logger.debug("Key exported")
