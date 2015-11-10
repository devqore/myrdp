# -*- coding: utf-8 -*-
from PyQt4 import QtGui


def addActionWithScreenChose(menu, slot, iconPath, actionName):
    """
    :param menu: QMenu to add action (or menu with actions containing detected screens)
    :param slot: slot to connect with parameter screenIndex
    :param iconPath: path to icon
    :param actionName: action name to add
    """
    ico = QtGui.QIcon(iconPath)
    screenCount = QtGui.QApplication.desktop().screenCount()
    if screenCount == 1:
        menu.addAction(ico, actionName, lambda: slot(screenIndex=0))
    else:
        screensMenu = menu.addMenu(ico, actionName)
        for screen in range(screenCount):
            # when lambda was without fix parameter, each method connectFrameless was run with latest screen :/
            screensMenu.addAction("Screen %s" % screen, lambda fix=screen: slot(screenIndex=fix))
