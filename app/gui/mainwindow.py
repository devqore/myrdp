# -*- coding: utf-8 -*-
from PyQt4.QtCore import QProcess, QSettings, Qt
from PyQt4.QtGui import QMainWindow, QWidget, QMessageBox, QMenu

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
        self.hostMenu.addAction("Connect frameless", self.connectFrameless)

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

    def showFramelessWidget(self):
        self.t.show()
        self.t.setGeometry(self.frameGeometry())

    def getCurrentHostListItemName(self):
        return self.ui.hostsList.currentItem().text()

    def findHostItemByName(self, name):
        result = self.ui.hostsList.findItems(name, Qt.MatchExactly)
        resultLen = len(result)
        if resultLen != 1:  # should be only one host
            logging.error("Host not found. Got %d results" % resultLen)
        return result[0]

    def slotShowHostContextMenu(self, pos):
        """ slot needed to show menu in proper position, or i'm doing something wrong
        """
        self.hostMenu.exec_(self.ui.hostsList.mapToGlobal(pos))

    def addHost(self):
        hostDialog = HostConfigDialog(self.hosts)
        resp = hostDialog.add()
        if resp["code"]:
            self.setHostList()
        hostName = resp.get("name")
        if hostName:
            hostItem = self.findHostItemByName(hostName)
            self.slotConnectHost(hostItem)

    def editHost(self):
        hostDialog = HostConfigDialog(self.hosts)
        resp = hostDialog.edit(self.getCurrentHostListItemName())
        if resp["code"]:
            self.setHostList()

    def deleteHost(self):
        self.hosts.delete(self.getCurrentHostListItemName())
        self.setHostList()

    def connectFrameless(self):
        self.connectHost(self.getCurrentHostListItemName(), frameless=True)

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
        self.connectHost(unicode(item.text()))

    def connectHost(self, hostId, frameless=False):
        hostId = unicode(hostId)  # sometimes hostId comes as QString
        tabPage = self.tabWidget.createTab(hostId)
        tabPage.reconnectionNeeded.connect(self.connectHost)

        if hostId in self.procs.keys():
            proc = self.procs[hostId]
            proc.kill()

        if frameless:
            self.tabWidget.detachFrameless(tabPage)

        execCmd, opts = self.getCmd(tabPage, hostId)
        self.startProcess(tabPage, hostId, execCmd, opts)

    def getCmd(self, tabPage, hostName):
        host = self.hosts.get(hostName)

        # set tabPage widget
        width, height = tabPage.setSizeAndGetCurrent()
        # 1et widget winId to embed rdesktop
        winId = tabPage.x11.winId()

        # set remote desktop client, at this time works only with freerdp
        remoteClientType, remoteClientOptions = self.config.getRdpClient()
        remoteClient = ClientFactory(remoteClientType, **remoteClientOptions)
        remoteClient.setWindowParameters(winId, width, height)
        remoteClient.setUserAndPassword(host.user, host.password)
        remoteClient.setAddress(host.address)
        return remoteClient.getComposedCommand()
    
    def startProcess(self, tabPage, hostId, execCmd, opts):
        """
        :param hostId:
        :param execCmd:
        :param opts: opts as list
        :return:
        """
        proc = QProcess()
        # todo: searching processes, with dictionary is monkey idea
        proc.stateChanged.connect(tabPage.slotStateChanged)
        proc.readyRead.connect(tabPage.slotRead)

        # when detached widget is closed
        tabPage.widgetClosed.connect(self.slotOnTabClosed)

        proc.setProcessChannelMode(QProcess.MergedChannels)
        proc.start(execCmd, opts)
        self.procs[hostId] = proc

    def saveSettings(self):
        settings = QSettings("MyRDP")
        settings.setValue("geometry", self.saveGeometry())
        settings.setValue("windowState", self.saveState())

    def restoreSettings(self):
        settings = QSettings("MyRDP")
        try:
            self.restoreGeometry(settings.value("geometry").toByteArray())
            self.restoreState(settings.value("windowState").toByteArray())
        except Exception:
            logging.debug("No settings to restore")

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
        # bug: workaround for bug when closing window and few tabs are opened with connected rdp
        for i in self.procs.values():
            try:
                i.kill()
            except:
                pass
        event.accept()

    def slotOnWidgetClosed(self, title):
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