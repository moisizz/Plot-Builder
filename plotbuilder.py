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
        self.plot.init_default_params()
    
    def set_dialog_const(self):
        cd = self.const_dialog.ui
        
        for key, value in self.plot.params.items():
            field = getattr(cd, key)
            field.setValue(value)
            
        cd.scaleX.setValue(self.plot.scale_x)
        cd.scaleY.setValue(self.plot.scale_y)
        cd.showGrid.setChecked(True)
        
        for plot in self.plot.plots.values():
            for line_name in plot.lines.keys():
                if hasattr(cd, line_name):
                    checkbox = getattr(cd, line_name)
                    checkbox.setChecked(plot.lines[line_name]['enabled'])
    
    #===================================Слоты====================================
        
    def draw_plot_slot(self):
        self.plot.start_animated_draw()
        
    def apply_const_slot(self):
        cd = self.const_dialog.ui
        self.plot.set_scale_x(cd.scaleX.value())
        self.plot.set_scale_y(cd.scaleY.value())
        self.plot.set_grid(cd.showGrid.isChecked())
        
        for key, value in self.plot.params.items():
            field = getattr(cd, key)
            value = field.value()
            self.plot.params[key] = value
                    
        if cd.lineType.isChecked():
            self.plot.set_draw_type('lines')
        elif cd.pointType.isChecked():
            self.plot.set_draw_type('points')
        
        for plot in self.plot.plots.values():
            for line_name in plot.lines.keys():
                if hasattr(cd, line_name):
                    checkbox = getattr(cd, line_name)
                    plot.lines[line_name]['enabled'] = checkbox.isChecked()        
        
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
