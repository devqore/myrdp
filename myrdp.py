# -*- coding: utf-8 -*-
from PyQt4.QtCore import *#QObject, SIGNAL, QProcess, QString, QStringList, QSettings, QUrl
from PyQt4.QtGui import *#QMainWindow, QMenu, QWidget, QMessageBox, QDesktopServices, QDialog
from mytabwidget import MyTabWidget
from config import Config
from myrdp_ui import Ui_MainWindow
from quickconnectdialog import QuickConnectDialog

import itertools


class MyRDP(QMainWindow):
    def __init__(self, config):
        super(MyRDP, self).__init__()
        self.configFile = config
        self.config = Config(self.configFile)
        self.initUi()
        self.setMenu()
        #to hold unique {hostId : proc}
        self.procs = {}
        self.restoreSettings()
    
    def initUi(self):
        self.ui = Ui_MainWindow()
        ui = self.ui
        
        ui.setupUi(self)
        self.tabWidget = MyTabWidget()
        self.setCentralWidget(self.tabWidget)
        
        #@todo: changing options and write to file with qdockwidget
        ui.optionsDock.hide()
        
        self.setHostList()
        
        QObject.connect(ui.hostsList, SIGNAL("itemDoubleClicked(QListWidgetItem*)"), self.slotConnectHost)
        QObject.connect(ui.hostsList, SIGNAL("itemClicked(QListWidgetItem*)"), self.slotShowHost)
        QObject.connect(self.tabWidget, SIGNAL("tabClosed(QString)"), self.slotOnTabClosed)
    
    #Fix to release keyboard from QX11EmbedContainer, when we leave widget through wm border      
    def leaveEvent(self, event):
        keyG = QWidget.keyboardGrabber()
        if keyG is not None:
            keyG.releaseKeyboard()
        event.accept()#needed?

    def setMenu(self):
        ui = self.ui
        menuList = QMenu()
        menuList.addAction("Reread config", self.slotRefreshList)
        menuList.addAction("Open config", self.openConfigFile)
        menuList.addAction("Quick connect", self.quickConnect)
        ui.menu.setMenu(menuList)
#        QObject.connect(ui.menu, SIGNAL("clicked()"), self.slotRefreshList)
    
    
    def openConfigFile(self):
        desk = QDesktopServices()
        desk.openUrl(QUrl("file://%s" % self.config.filePath))
    
    def slotRefreshList(self):
        self.config = Config(self.configFile)
        self.ui.hostsList.clear()
        self.setHostList()
       
    def setHostList(self):
        """ set hosts list in list view """
        self.ui.hostsList.addItems(QStringList(self.config.hosts))
    
    def slotShowHost(self, item):
        #on one click we activating tab and showing options
        self.tabWidget.activateTab(item)

    def slotConnectHost(self, item):     
        self.tabPage = self.tabWidget.createTab(item)
        
        hostId = str(item.text())
        if hostId in self.procs.keys():
            proc = self.procs[hostId]
            proc.kill()
        
        hostOptionsDict = self.config.getHostOptions(hostId)
        
        execCmd, opts = self.getCmd(hostOptionsDict)
        
        self.startProcess(hostId, execCmd, opts)
    
    def quickConnect(self):      
        qc = QuickConnectDialog()
        ret = qc.exec_()
        
        if ret == QDialog.Rejected:
            return

        #to add section in config
        quickHost = dict()
        
        #@todo: add validation in qdialog! host line edit cannot be empty
        #@todo: add checkbox to add element to config.ini
        #@todo: propably move all qc.ui...text() to quickconnectdialog class
        ip = qc.ui.host.text()
        quickHost["ip"] = str(ip) 
        hostName = self.config.getUniqueHost(ip)#section name
        
        #could be a function
        user = qc.ui.user.text()
        if user != "":
            quickHost["u"] = user
             
        passwd = qc.ui.password.text()
        if passwd != "":
            quickHost["p"] = passwd
            
        self.config.addHost(hostName, quickHost)
        
        #add item to host list and emit item clicked 
        item = QListWidgetItem(hostName)
        item.setBackground(Qt.gray)
        self.ui.hostsList.addItem(item)      
        self.ui.hostsList.emit(SIGNAL("itemDoubleClicked(QListWidgetItem*)"), item)
       
        
    def getCmd(self, hostOptionsDict):
        #ip allways as last argument
        try:
            ip = hostOptionsDict.pop("ip")
        except:
            print "Maybe you should give some ip or dns name?"
            return
        
        try:
            execCmd = hostOptionsDict.pop("exec")               
        except:
            execCmd = "rdesktop"
                
        opts = list(itertools.chain(*[("-" + k, v) for k, v in hostOptionsDict.items()]))
        
        #e.g: exec=rdesktop -a -b -c
        execCmdSplit = execCmd.split(" ")
        if len(execCmdSplit) > 1:
            opts.extend(execCmdSplit[1:])
            execCmd = execCmdSplit[0]
        
        #set geometry of rdesktop window to fill widget size, if geometry not set in config file
        if "-g" not in opts:
            geom = self.tabPage.setSize()
            opts.extend(["-g", geom])

        #get widget winId to embed rdesktop 
        winId = self.tabPage.x11.winId()
        opts.extend(["-X", QString.number(winId)])

        #at least append id        
        opts.append(ip)        
        return execCmd, opts
    
    def startProcess(self, hostId, execCmd, opts):
        proc = QProcess()
        #@todo: searching processes, with dictionary is monkey idea
#        proc.setObjectName(u"proc_%s" % hostId)
        QObject.connect(proc, SIGNAL("stateChanged(QProcess::ProcessState)"), self.tabPage.slotStateChanged)
        QObject.connect(proc, SIGNAL("readyRead()"), self.tabPage.slotRead)
        #when detached widget is closed
        QObject.connect(self.tabPage, SIGNAL("widgetClosed(QString)"), self.slotOnTabClosed)
        
        proc.setProcessChannelMode(QProcess.MergedChannels)
        proc.start(execCmd, QStringList(opts))
        self.procs[hostId] = proc

    def saveSettings(self):
        settings = QSettings("MyRDP");
        settings.setValue("geometry", self.saveGeometry());
        settings.setValue("windowState", self.saveState());

    def restoreSettings(self):
        settings = QSettings("MyRDP");
        self.restoreGeometry(settings.value("geometry").toByteArray());
        self.restoreState(settings.value("windowState").toByteArray());

    def closeEvent(self, event):
        #@todo: ask on close when has tabs should go as option, by default turned on
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
        #@bug: workaraound for bug when closing window and few tabs are opened with connected rdp
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
        #@todo: search processes
        #@BUG: odlaczasz hosta, nastepnie robisz reconnect na odlaczaonym i zamykasz karte
        #i jebs probuje ubic dwa razy proces, rozwiazaniem byloby wyszukiwanie prcesow zamiast 
        #uzupelnianie samemu slownika
        try:
            proc = self.procs.pop(u"%s" % title)
            proc.kill()
        except:
            pass
        