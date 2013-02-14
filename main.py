# -*- coding: utf-8 -*-
#from PyQt4 import QtCore
#from PyQt4.uic.Compiler.qtproxies import QtCore
from PyQt4.QtGui import QApplication
from myrdp import MyRDP 
import sys
#import sip #sip needed to build with bb-ffreeze

#@todo: opt parse

if __name__ == "__main__":   
    app = QApplication(sys.argv)
    mw = MyRDP()   
    mw.show()
    sys.exit(app.exec_())