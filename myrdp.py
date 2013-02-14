# -*- coding: utf-8 -*-
from PyQt4.QtCore import QObject, SIGNAL, QProcess, QString, QStringList
from PyQt4.QtGui import QMainWindow, QMenu
from mytabwidget import MyTabWidget
from config import Config
from myrdp_ui import Ui_MainWindow

import itertools

class MyRDP(QMainWindow):
    def __init__(self):
        super(MyRDP, self).__init__()
        self.config = Config()
        self.initUi()
        self.setMenu()
        #to hold unique {hostId : proc}
        self.procs = {}
        self.setMouseTracking(True)
        
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

    def setMenu(self):
        ui = self.ui
        menuList = QMenu()
        menuList.addAction("Reread config.ini", self.slotRefreshList)
        ui.menu.setMenu(menuList)
#        QObject.connect(ui.menu, SIGNAL("clicked()"), self.slotRefreshList)
    
    def slotRefreshList(self):
        self.config = Config()
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
        
        #@todo: create some function to set config, this mess is to long
        hostOptionsDict = self.config.getHostOptions(hostId)
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
        
#    def slotRead(self):
#        print "from slog", self.proc.readAllStandardOutput()

    def closeEvent(self, event):
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
        