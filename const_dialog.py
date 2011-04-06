# -*- coding: utf8 -*-

from PyQt4.QtCore import *
from PyQt4 import QtGui

from const_dialog_ui import Ui_Dialog

class ConstDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)