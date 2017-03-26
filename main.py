# -*- coding: utf-8 -*-
import sys
import signal

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QWidget, QApplication

from app.log import logger
from app.config import Config
from app.database import Database

from app.gui.mainwindow import MainWindow
from app.gui.mytabwidget import X11Embed

from argparse import ArgumentParser


def argParser():
    parser = ArgumentParser(description='MyRDP')    
    parser.add_argument("-c", "--config", default="config.yaml", help='config file (default: config.yaml)')
    return parser.parse_args()


def focusChanged(lostFocus, hasFocus):
    hasFocusType = type(hasFocus)
    if hasFocus is None or hasFocusType != X11Embed:  # for e.g. focus is out from application, or is another widget
        keyG = QWidget.keyboardGrabber()  # find keyboardGrabber and releaseKeyboard
        if keyG is not None:
            keyG.releaseKeyboard()
    elif hasFocusType == X11Embed:
        hasFocus.grabKeyboard()

if __name__ == "__main__":   
    args = argParser()
    app = QApplication(sys.argv)
    # show icons in menus
    app.setAttribute(Qt.AA_DontShowIconsInMenus, False)

    # finish app with ctrl+c
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app.focusChanged.connect(focusChanged)

    config = Config(args.config)

    db = Database(config.getConnectionString())
    db.create()
    db.update()

    logger.setLevel(config.getLogLevel())

    mw = MainWindow(config)
    mw.show()

    app.exec_()
    app.deleteLater()
    sys.exit(0)
