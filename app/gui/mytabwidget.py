# -*- coding: utf-8 -*-
from PyQt4.QtCore import pyqtSignal, Qt, qDebug
from PyQt4 import QtGui


class X11Embed(QtGui.QX11EmbedContainer):
    def __init__(self, parent=None):
        super(X11Embed, self).__init__(parent)
        self.setMouseTracking(True)
        self.setMinimumSize(200, 200)


class ControlButton(QtGui.QPushButton):
    offset = None

    def __init__(self, pageTabParent):
        super(ControlButton, self).__init__(pageTabParent)
        self.w = 25
        self.h = 25
        # self.setStyleSheet("* {background: transparent;}")
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setGeometry(pageTabParent.width() - self.w, pageTabParent.height() - self.h, self.w, self.h)
        self.show()

    def mousePressEvent(self, event):
        self.offset = event.pos()
        super(ControlButton, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        position = self.mapToParent(event.pos() - self.offset)
        geometry = self.geometry()

        x = position.x()
        y = position.y()

        parentGeometry = self.parent().geometry()
        maxX = parentGeometry.width() - geometry.width()
        maxY = parentGeometry.height() - geometry.height()

        # set max and minimum X,Y area
        if x < 0:
            x = 0
        elif x > maxX:
            x = maxX

        if y < 0:
            y = 0
        elif y > maxY:
            y = maxY

        # todo: move snapped only to borders
        self.move(x, y)


class PageTab(QtGui.QWidget):
    widgetClosed = pyqtSignal("QString")
    controlButton = None
    showControlButtonWhenDetached = True
    reconnectionNeeded = pyqtSignal("QString")

    def __init__(self, parent=None):
        super(PageTab, self).__init__(parent)
        # used for check if process has been stoped
        self.lastState = None
        
        self.layout = QtGui.QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # bellow each rdesktop instance is text area with stdout/stderr debug
        # if somenthing goes wrong text is visible, but when rdesktop is runnig
        # current display area is covered by rdp.
        # If window is resized, thereis a lot of text, and rdp size is smaller,
        # than display area, you can see the text ;) looks buggy but at this (any:P) time
        # i think that's not important :)

        self.textEdit = QtGui.QTextEdit(self)
        self.textEdit.setReadOnly(True)
        self.textEdit.setFrameShape(QtGui.QFrame.NoFrame)
        self.textEdit.setStyleSheet("background-color:transparent;")
        
        self.textEdit.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textEdit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
    
        self.layout.addWidget(self.textEdit)

        # to embed rdesktop, if we use QWidget, there is some problems with
        # shortcuts (for e.g. in xfwm4), with QX11EmbedContainer looks good 
        self.x11 = X11Embed(self)

    def showControlButton(self):
        if not self.controlButton and self.showControlButtonWhenDetached:
            self.controlButton = ControlButton(self)
            menu = QtGui.QMenu()
            menu.addAction("Close", self.close)
            menu.addAction("Reconnect", self.emitReconnect)
            self.controlButton.setMenu(menu)

    def closeEvent(self, event):
        title = self.windowTitle()
        self.widgetClosed.emit(title)
        event.accept()
        self.deleteLater()

    def setSizeAndGetCurrent(self):
        """ Sets size of QX11EmbedContainer, because QX11 is not in layout, but
            textEdit is. Returns size of textEdit area which will be used in remote client
        """
        self.x11.setFixedSize(self.textEdit.size())
        return self.textEdit.width(), self.textEdit.height()

    def slotRead(self):
        proc = self.sender() 
        txt = proc.readAllStandardOutput()
        qDebug(txt) 
        self.textEdit.append(txt.data().rstrip('\n'))
#        self.autoScroll()

    def slotStateChanged(self, state):
        # QProcess::NotRunning - 0
        # QProcess::Starting - 1
        # QProcess::Running - 2
        # append text to the text area only when process has been stopped
        if state == 0 and self.lastState == 2:
            self.textEdit.append("<i>Process has been stopped..</i><br />")
        self.lastState = state
        
    def text(self):
        return self.windowTitle()

    def emitReconnect(self):
        self.reconnectionNeeded.emit(self.text())


class MyTabWidget(QtGui.QTabWidget):
    # to communicate with main window, and send signal with tabName
    tabClosed = pyqtSignal("QString")

    def __init__(self):
        super(MyTabWidget, self).__init__()
        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.slotCloseTab)
        self.setStyleSheet("""QTabBar::tab:selected, QTabBar::tab:hover { 
                              background: 
                                qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, 
                                    stop: 0 # fafafa, 
                                    stop: 0.4 # f4f4f4,
                                    stop: 0.5 # e7e7e7,
                                    stop: 1.0 # fafafa); }""")
        self.setMovable(True)
        self.setTab()
        # used when chosing action from menu 
        self.currentTabIdx = None
        
        # list with detached windows
        self.detached = {}
       
    def setTab(self):
        self.tab = self.tabBar()
        self.tab.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tab.customContextMenuRequested.connect(self.showContextMenu)

        self.popMenu = QtGui.QMenu(self)
        self.popMenu.addAction("Detach tab", self.detach)
        self.popMenu.addAction("Detach frameless", self.detachFrameless)
#        self.popMenu.addAction("Reconnect", self.reconnect)

    def showContextMenu(self, point):
        self.currentTabIdx = self.tab.tabAt(point)
        self.popMenu.exec_(self.tab.mapToGlobal(point))

    def setDetached(self, frameless, widget=None):
        if not widget:
            widget = self.widget(self.currentTabIdx)
        widget.setParent(None)

        if frameless:
            widget.setWindowFlags(Qt.FramelessWindowHint)
        widget.setWindowIcon(QtGui.QIcon(":/ico/myrdp.svg"))
        widget.show()

        # temp hack to not delete object, because will delete after show
        # todo: do it better
        title = widget.windowTitle()
        self.detached[title] = widget

        if frameless:
            widget.setGeometry(self.parent().frameGeometry())
            widget.reconnectionNeeded.emit(title)

        widget.showControlButton()

    def detach(self, widget=None):
        self.setDetached(False, widget)

    def detachFrameless(self, widget=None):
        self.setDetached(True, widget)

    def getTabObjectName(self, tabName):
        return u"p_%s" % tabName
    
    def createTab(self, tabName):
        # used for create unique object name (because title is unique)
        tabObjectName = self.getTabObjectName(tabName)
#        tabWidget = self.findChild(QX11EmbedContainer, tabObjectName)
        tabWidget = self.findChild(PageTab, tabObjectName)
        
        for topLevel in QtGui.QApplication.topLevelWidgets():
            if type(topLevel) == PageTab and topLevel.objectName() == tabObjectName:
                    return topLevel
        
        if tabWidget is None:
            # todo: maybe we should use scroll area? but why? if size doesn`t fit, just reconnect
            newTab = PageTab(self)
            newTab.setObjectName(tabObjectName)
            tabIdx = self.addTab(newTab, tabName)
            newTab.setWindowTitle(tabName)
            self.setCurrentIndex(tabIdx)
            return newTab
        else:
            return tabWidget
        
    def activateTab(self, hostId):
        tabName = self.getTabObjectName(hostId)
        tabWidget = self.findChild(PageTab, tabName)
        
        if tabWidget is not None:
            tabIdx = self.indexOf(tabWidget)
            self.setCurrentIndex(tabIdx)
    
    def slotCloseTab(self, tabIdx):
        tabTitle = self.tabText(tabIdx)
        tabWidget = self.widget(tabIdx)
        self.tabClosed.emit(tabTitle)
        self.removeTab(tabIdx)
        tabWidget.deleteLater()