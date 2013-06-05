# -*- coding: utf-8 -*-
from PyQt4.QtGui import QDialog
from quickconnect_ui import Ui_QuickConnectDialog

class QuickConnectDialog(QDialog):
    def __init__(self):
        super(QuickConnectDialog, self).__init__()
        self.ui = Ui_QuickConnectDialog()
        self.ui.setupUi(self)
