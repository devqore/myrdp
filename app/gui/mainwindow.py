# -*- coding: utf-8 -*-
from PyQt4.QtCore import QProcess, QSettings
from PyQt4.QtGui import QDialog, QMainWindow, QWidget, QMessageBox, QMenu

from app import logging
from app.config import Config
from app.client import ClientFactory
from app.database import Database
from app.hosts import Hosts
from app.gui.hostconfig import HostConfigDialog
from app.gui.mainwindow_ui import Ui_MainWindow
from app.gui.mytabwidget import MyTabWidget


class MainWindow(QMainWindow):
    def __init__(self, config):
        super(MainWindow, self).__init__()
        self.config = Config(config)
        db = Database(self.config.getConnectionString())
        db.create()
        self.hosts = Hosts(db)

        # menu used for each host
        self.hostMenu = QMenu()
        self.hostMenu.addAction("Edit", self.editHost)
        self.hostMenu.addAction("Delete", self.deleteHost)

        # setup main window
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.addHost.clicked.connect(self.addHost)

        # set events on hosts list
        self.ui.hostsList.itemDoubleClicked.connect(self.slotConnectHost)
        self.ui.hostsList.itemClicked.connect(self.slotShowHost)
        self.ui.hostsList.customContextMenuRequested.connect(self.slotShowHostContextMenu)

        # set tab widget
        self.tabWidget = MyTabWidget()
        self.setCentralWidget(self.tabWidget)
        self.tabWidget.tabClosed.connect(self.slotOnTabClosed)

        self.setHostList()

        # to hold unique {hostId : proc}
        self.procs = {}
        self.restoreSettings()

    def getCurrentHostListItemName(self):
        return self.ui.hostsList.currentItem().text()

    def slotShowHostContextMenu(self, pos):
        """ slot needed to show menu in proper position, or i'm doing something wrong
        """
        self.hostMenu.exec_(self.ui.hostsList.mapToGlobal(pos))

    def addHost(self):
        hostDialog = HostConfigDialog(self.hosts)
        resp = hostDialog.add()
        if resp:
            self.setHostList()

    def editHost(self):
        hostDialog = HostConfigDialog(self.hosts)
        resp = hostDialog.edit(self.getCurrentHostListItemName())
        if resp:
            self.setHostList()

    def deleteHost(self):
        self.hosts.delete(self.getCurrentHostListItemName())
        self.setHostList()

    # Fix to release keyboard from QX11EmbedContainer, when we leave widget through wm border
    def leaveEvent(self, event):
        keyG = QWidget.keyboardGrabber()
        if keyG is not None:
            keyG.releaseKeyboard()
        event.accept()  # needed?

    def setHostList(self):
        """ set hosts list in list view """
        logging.debug("Setting hosts list")
        self.ui.hostsList.clear()
        self.ui.hostsList.addItems(self.hosts.getAllHostsNames())
    
    def slotShowHost(self, item):
        # on one click we activating tab and showing options
        self.tabWidget.activateTab(item)

    def slotConnectHost(self, item):
        self.tabPage = self.tabWidget.createTab(item)
        
        hostId = unicode(item.text())
        if hostId in self.procs.keys():
            proc = self.procs[hostId]
            proc.kill()

        execCmd, opts = self.getCmd(hostId)
        self.startProcess(hostId, execCmd, opts)

    def getCmd(self, hostName):
        host = self.hosts.get(hostName)

        # set tabPage widget
        width, height = self.tabPage.setSizeAndGetCurrent()
        # 1et widget winId to embed rdesktop
        winId = self.tabPage.x11.winId()

        # set remote desktop client, at this time works only with freerdp
        remoteClientType, remoteClientOptions = self.config.getRdpClient()
        remoteClient = ClientFactory(remoteClientType, **remoteClientOptions)
        remoteClient.setWindowParameters(winId, width, height)
        remoteClient.setUserAndPassword(host.user, host.password)
        remoteClient.setAddress(host.address)
        return remoteClient.getComposedCommand()
    
    def startProcess(self, hostId, execCmd, opts):
        """
        :param hostId:
        :param execCmd:
        :param opts: opts as list
        :return:
        """
        proc = QProcess()
        # todo: searching processes, with dictionary is monkey idea
#        proc.setObjectName(u"proc_%s" % hostId)
        proc.stateChanged.connect(self.tabPage.slotStateChanged)
        proc.readyRead.connect(self.tabPage.slotRead)

        # when detached widget is closed
        self.tabPage.widgetClosed.connect(self.slotOnTabClosed)

        proc.setProcessChannelMode(QProcess.MergedChannels)
        proc.start(execCmd, opts)
        self.procs[hostId] = proc

    def saveSettings(self):
        settings = QSettings("MyRDP")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())

    def restoreSettings(self):
        settings = QSettings("MyRDP")
        self.restoreGeometry(settings.value("geometry").toByteArray())
        self.restoreState(settings.value("windowState").toByteArray())

    def closeEvent(self, event):
        # todo: ask on close when has tabs should go as option, by default turned on
        if self.tabWidget.count() == 0:
            self.saveSettings()
            return
               
        msgBox = QMessageBox(self, text="Are you soure do you want to quit?")
        msgBox.setWindowTitle("Exit confirmation")
        msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        ret = msgBox.exec_()
        if ret == QMessageBox.Cancel:
            event.ignore()
            return
        
        self.saveSettings()
        # bug: workaraound for bug when closing window and few tabs are opened with connected rdp
        for i in self.procs.values():
            try:
                i.kill()
            except:
                pass
        event.accept()

    def slotOnWigetClosed(self, title):
        self.tabWidget.detached.pop(u"%s" % title)
        self.slotOnTabClosed(title)

    def slotOnTabClosed(self, title):
        try:
            proc = self.procs.pop(u"%s" % title)
            proc.kill()
        except:
            # bug: after detaching tab make reconnect, after that close the tab.
            # Make just pass until Process class is not refactored
            pass