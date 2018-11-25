# -*- coding: utf-8 -*-
from PyQt4.QtGui import QDialog
from app.gui.groupmanager_ui import Ui_GroupManager


class GroupManager(QDialog):
    def __init__(self):
        super(GroupManager, self).__init__()
        self.ui = Ui_GroupManager()
        self.ui.setupUi(self)
