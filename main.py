# -*- coding: utf-8 -*-
from PyQt4.QtGui import QWidget, QApplication
import sys

from app.gui.mainwindow import MainWindow
from app.gui.mytabwidget import X11Embed

# import sip # sip needed to build with bb-ffreeze
from argparse import ArgumentParser


def argParser():
    parser = ArgumentParser(description='MyRDP')    
    parser.add_argument("-c", "--config", default="config.yaml", help='config file (default: config.ini)')
    return parser.parse_args()


def focusChanged(lostFocus, hasFocus):
    hasFocusType = type(hasFocus)
    if hasFocus is None or hasFocusType != X11Embed: # for e.g. focus is out from application, or is another widget
        keyG = QWidget.keyboardGrabber()  # find keyboardGraber and releaseKeyboard
        if keyG is not None:
            keyG.releaseKeyboard()
    elif hasFocusType == X11Embed:
        hasFocus.grabKeyboard()

if __name__ == "__main__":   
    args = argParser()
    app = QApplication(sys.argv)

    app.focusChanged.connect(focusChanged)

    mw = MainWindow(args.config)
    mw.show()
    sys.exit(app.exec_())