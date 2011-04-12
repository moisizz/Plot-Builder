# -*- coding: utf8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from form_ui import Ui_MainWindow
from const_dialog import ConstDialog
from plot import PlotCanvas

#Класс построителя графиков
class PlotBuildApplication(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.centralWidget.setLayout(self.ui.plotArea)
        
        self.plot = PlotCanvas(self.ui.centralWidget)
        self.toolbar = NavigationToolbar(self.plot, self)
        self.ui.plotArea.addWidget(self.toolbar)
        self.ui.plotArea.addWidget(self.plot)
        
        self.const_dialog = ConstDialog()
        self.set_dialog_const()
        
        self.connect(self.ui.constEditAction, SIGNAL('activated()'), self.edit_constant_slot)
        self.connect(self.ui.calculateAction, SIGNAL('activated()'), self.draw_plot_slot)
        
        self.connect(self.const_dialog.ui.applyButton, SIGNAL('clicked()'), self.apply_const_slot)
        self.connect(self.const_dialog.ui.resetButton, SIGNAL('clicked()'), self.reset_const_slot)
    
    def const_init(self):
        self.plot.set_time_limit(20)       
        self.plot.set_scale_x(1)
        self.plot.set_scale_y(1)
        self.plot.set_integr_step(0.1)
        self.plot.set_k(0.005)
        self.plot.set_m(0.05)
    
    def set_dialog_const(self):
        cd = self.const_dialog.ui
        cd.parameterK.setValue(self.plot.k)
        cd.parameterM.setValue(self.plot.m)
        cd.time.setValue(self.plot.time_limit)
        cd.integrStep.setValue(self.plot.integr_step)
        cd.scaleX.setValue(self.plot.scale_x)
        cd.scaleY.setValue(self.plot.scale_y)
    
    #===================================Слоты====================================
        
    def draw_plot_slot(self):
        self.plot.draw_plot()
        
    def apply_const_slot(self):
        cd = self.const_dialog.ui
        
        self.plot.set_time_limit(cd.time.value())       
        self.plot.set_scale_x(cd.scaleX.value())
        self.plot.set_scale_y(cd.scaleY.value())
        self.plot.set_integr_step(cd.integrStep.value())
        self.plot.set_k(cd.parameterK.value())
        self.plot.set_m(cd.parameterM.value())
        
        self.plot.draw_plot()
    
    def reset_const_slot(self):
        self.const_init()
        self.set_dialog_const()
        
        self.plot.draw_plot()
        
    def edit_constant_slot(self):
        self.set_dialog_const()        
        self.const_dialog.show()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    PlotBuilder = PlotBuildApplication()
    PlotBuilder.show()
    sys.exit(app.exec_())
