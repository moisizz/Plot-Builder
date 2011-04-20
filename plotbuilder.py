# -*- coding: utf8 -*-

import sys
import os
from PyQt4.QtCore import SIGNAL
from PyQt4 import QtGui
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar

from form import Ui_MainWindow
from const_dialog import Ui_Dialog
from plot import Oscillator


class ConstDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

class PlotBuildApplication(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.centralWidget.setLayout(self.ui.plotArea)
        
        self.plot = Oscillator(self.ui.centralWidget)
        self.ui.plotArea.addWidget(self.plot)
        
        self.const_dialog = ConstDialog(self)
        self.set_dialog_const()
        
        self.connect(self.ui.constEditAction, SIGNAL('activated()'), self.edit_constant_slot)
        self.connect(self.ui.calculateAction, SIGNAL('activated()'), self.draw_plot_slot)
        self.connect(self.ui.saveImageAction, SIGNAL('activated()'), self.save_plot_image_slot)
        
        self.connect(self.const_dialog.ui.applyButton, SIGNAL('clicked()'), self.apply_const_slot)
        self.connect(self.const_dialog.ui.resetButton, SIGNAL('clicked()'), self.reset_const_slot)
    
    def const_init(self):
        self.plot.set_time_limit(42)       
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
        cd.showGrid.setChecked(True)
    
    #===================================Слоты====================================
        
    def draw_plot_slot(self):
        self.plot.start_animated_draw()
        
    def apply_const_slot(self):
        cd = self.const_dialog.ui
        
        self.plot.set_time_limit(cd.time.value())       
        self.plot.set_scale_x(cd.scaleX.value())
        self.plot.set_scale_y(cd.scaleY.value())
        self.plot.set_integr_step(cd.integrStep.value())
        self.plot.set_k(cd.parameterK.value())
        self.plot.set_m(cd.parameterM.value())
        self.plot.set_grid(cd.showGrid.isChecked())      
        
        if cd.lineTypeButton.isChecked():
            self.plot.set_draw_type('lines')
        elif cd.pointTypeButton.isChecked():
            self.plot.set_draw_type('points')
        
        self.plot.switch_line('wave', 'canonical_t_x', cd.canonical_t_x.isChecked())
        self.plot.switch_line('wave', 'canonical_t_v', cd.canonical_t_v.isChecked())
        
        self.plot.switch_line('wave', 'eiler_t_x', cd.eiler_t_x.isChecked())
        self.plot.switch_line('wave', 'eiler_t_v', cd.eiler_t_v.isChecked())
        
        self.plot.switch_line('wave', 'vxxv_t_x', cd.vxxv_t_x.isChecked())
        self.plot.switch_line('wave', 'vxxv_t_v', cd.vxxv_t_v.isChecked())
        
        self.plot.switch_line('wave', 'canonical_t_dh', cd.canonical_t_h.isChecked())
        self.plot.switch_line('wave', 'eiler_t_dh', cd.eiler_t_h.isChecked())
        self.plot.switch_line('wave', 'vxxv_t_dh', cd.vxxv_t_h.isChecked())

        self.plot.switch_line('circle', 'canonical_x_v', cd.canonical_x_v.isChecked())
        self.plot.switch_line('circle', 'eiler_x_v', cd.eiler_x_v.isChecked())
        self.plot.switch_line('circle', 'vxxv_x_v', cd.vxxv_x_v.isChecked())
        
        
        self.plot.start_animated_draw()
    
    def reset_const_slot(self):
        self.const_init()
        self.set_dialog_const()
        
        self.plot.start_animated_draw()
        
    def edit_constant_slot(self):
        self.set_dialog_const()        
        self.const_dialog.show()

    def save_plot_image_slot(self):
        path = QtGui.QFileDialog.getExistingDirectory()
    
        if path:
            self.plot.save_plots(path)
        

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    PlotBuilder = PlotBuildApplication()
    PlotBuilder.show()
    sys.exit(app.exec_())
