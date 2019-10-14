# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4.QtGui import QWidget, QFileDialog, QMenu
from app.gui.settings_ui import Ui_SettingsPage
from app.gui.setkeypassword import SetKeyPassword
from app.config import Config


class SettingsPage(QWidget):
    def __init__(self):
        super(SettingsPage, self).__init__()
        self.ui = Ui_SettingsPage()
        self.ui.setupUi(self)
        self.ui.information_label.setVisible(False)
        self.ui.database_location_button.clicked.connect(self.selectDatabaseLocation)
        self.ui.freerdp_executable_button.clicked.connect(self.selectFreerdpLocation)
        self.ui.save_button.clicked.connect(self.saveSettings)

        self.config = Config()
        self.ui.database_location.setText(self.config.database_location)
        self.ui.freerdp_executable.setText(self.config.freerdp_executable)
        self.ui.freerdp_arguments.setText(self.config.freerdp_args)

        self.keyMenu = QMenu()
        self.keyMenu.addAction('Set master password', self.setKeyPassword)
        self.ui.master_key_button.setStyleSheet("QPushButton::menu-indicator {image: none;}")
        self.ui.master_key_button.setMenu(self.keyMenu)

        self.ui.logging_level.addItems(self.config.logging_levels)
        currentItem = self.ui.logging_level.findText(self.config.log_level)
        if currentItem != -1:
            self.ui.logging_level.setCurrentIndex(currentItem)

    @staticmethod
    def setKeyPassword():
        skp = SetKeyPassword()
        skp.exec_()

    def selectFreerdpLocation(self):
        dialog = QFileDialog()
        result = dialog.getOpenFileName(self, "Freerdp location", directory='/usr/bin')
        if result != QtCore.QString(''):
            self.ui.freerdp_executable.setText(result)

    def selectDatabaseLocation(self):
        dialog = QFileDialog()
        dialog.setFileMode(QFileDialog.AnyFile)
        result = dialog.getSaveFileName(self, "Database location", filter="*.sqlite")
        if result != QtCore.QString(''):
            self.ui.database_location.setText(result)

    def saveSettings(self):
        databaseLocationToSave = self.ui.database_location.text()
        if self.config.database_location != databaseLocationToSave:
            self.config.set_database_location(self.ui.database_location.text())
            self.ui.information_label.setVisible(True)
        self.config.set_freerdp_executable(self.ui.freerdp_executable.text())
        self.config.set_freerdp_args(self.ui.freerdp_arguments.text())
        self.config.set_log_level(self.ui.logging_level.currentText())