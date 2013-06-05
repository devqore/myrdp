# -*- coding: utf-8 -*-
#from PyQt4 import QtCore
#from PyQt4.uic.Compiler.qtproxies import QtCore
from PyQt4.QtGui import QApplication, QWidget
from myrdp import MyRDP 
from mytabwidget import X11Embed
import sys
#import sip #sip needed to build with bb-ffreeze

#@todo: opt parse
from argparse import ArgumentParser

def argParser():
    parser = ArgumentParser(description='MyRDP')    
    parser.add_argument("-c", "--config", default="config.ini", help='config file (default: config.ini)')    
    return parser.parse_args()


from PyQt4.QtCore import QObject, SIGNAL
def focusChanged(lostFocus, hasFocus):
    hasFocusType = type(hasFocus)
    if hasFocus is None or hasFocusType != X11Embed:#for e.g. focus is out from application, or is another widget
        keyG = QWidget.keyboardGrabber() #find keyboardGraber and releaseKeyboard
        if keyG is not None:
            keyG.releaseKeyboard()            
    elif hasFocusType == X11Embed:
        #hasFocus.underMouse() with X11EmbedContainter underMouse doesnt work :(
        hasFocus.grabKeyboard()
    

if __name__ == "__main__":   
    args = argParser()
    app = QApplication(sys.argv)
    
    QObject.connect(app, SIGNAL("focusChanged(QWidget*, QWidget*)"), focusChanged)
    
    mw = MyRDP(args.config)   
    mw.show()
    sys.exit(app.exec_())