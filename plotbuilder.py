
# -*- coding: utf8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4 import QtGui

from numpy import arange, pi, abs
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure

import curives
from form import Ui_MainWindow

#Холст плоского графика
class PlotCanvas(FigureCanvas):
    #Конструктор
    def __init__(self, parent=None, line_func=curives.pascal_snail, arg_min=-1, arg_max=1):
        self.min_axis_x = -10
        self.max_axis_x = 10
        self.min_axis_y = -5
        self.max_axis_y = 5
        
        self.scale_x = 1
        self.scale_y = 1
        
        self.accuracy = 0.001
        self.cross_axes = arange(-10, 10, self.accuracy)
        
        self.arg_min = arg_min
        self.arg_max = arg_max
        
        self.figure = Figure(figsize=(100, 100), facecolor="white")
        self.axes = self.figure.add_subplot(111)
        self.line_function = line_func
        
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.draw_plot()

    #Изменение границ отображения осей
    def set_x_axis_min(self, value):
        self.min_axis_x = value

    def set_x_axis_max(self, value):
        self.max_axis_x = value

    def set_y_axis_min(self, value):
        self.min_axis_y = value

    def set_y_axis_max(self, value):
        self.max_axis_x = value

    #Изменение масштаба
    def set_scale_x(self, value):
        self.scale_x = value

    def set_scale_y(self, value):
        self.scale_y = value

    #Изменение границ области определения аргумента
    def set_arg_min(self, value):
        self.arg_min = value

    def set_arg_max(self, value):
        self.arg_max = value

    def set_accuracy(self, value):
        self.accuracy = value

    def set_line_function(self, func):
        self.line_function = func

    #Отрисовка фигуры (не отображение)
    def draw_plot(self):
        self.axes.clear()
    
        self.axes.set_title("X: 1:%.1f   Y: 1:%.1f" % (self.scale_x, self.scale_y))
        self.axes.set_xticks(arange(-100,100,1))
        self.axes.set_yticks(arange(-100,100,1))
    
        self.axes.set_xlim(self.min_axis_x, self.max_axis_x)
        self.axes.set_ylim(self.min_axis_y, self.max_axis_y)
        self.axes.grid(True)
    
        for label in self.axes.xaxis.get_ticklabels():
            label.set_fontsize(8)
        for label in self.axes.yaxis.get_ticklabels():
            label.set_fontsize(8)
    
        (x, y) = self.line_function(arange(self.arg_min, self.arg_max, self.accuracy))
        (x, y) = (self.scale_x*x, self.scale_y*y)
    
        self.axes.plot(x, y)
        self.axes.plot([-10, 10], [0, 0], color="black")
        self.axes.plot([0, 0], [-10, 10], color="black")
        self.draw()


#Класс построителя графиков
class PlotBuildApplication(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.centralWidget.setLayout(self.ui.plotArea)
    
        self.plot = PlotCanvas(self.ui.centralWidget, arg_min=0, arg_max=2*pi)
        self.toolbar = NavigationToolbar(self.plot, self)
        self.ui.plotArea.addWidget(self.toolbar)
        self.ui.plotArea.addWidget(self.plot)
        self.ui.intervalMin.setValue(self.plot.arg_min);
        self.ui.intervalMax.setValue(self.plot.arg_max);
    
        self.connect(self.ui.circleAction, SIGNAL("activated()"), lambda func=curives.circle, arg_min=0, arg_max=2*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.cardioidAction, SIGNAL("activated()"), lambda func=curives.cardioid, arg_min=0, arg_max=2*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.astroidAction, SIGNAL("activated()"), lambda func=curives.astroid, arg_min=0, arg_max=2*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.deltoidAction, SIGNAL("activated()"), lambda func=curives.deltoid, arg_min=0, arg_max=2*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.hypocycloidAction, SIGNAL("activated()"), lambda func=curives.hypocycloid, arg_min=0, arg_max=4*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.bernLeminiskateAction, SIGNAL("activated()"), lambda func=curives.bern_leminiskate, arg_min=-20*pi, arg_max=20*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.jeronLeminiskatAction, SIGNAL("activated()"), lambda func=curives.jeron_leminiskate, arg_min=-20*pi, arg_max=20*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.logSpiralAction, SIGNAL("activated()"), lambda func=curives.log_spiral, arg_min=-20*pi, arg_max=20*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.nefroidAction, SIGNAL("activated()"), lambda func=curives.nefroid, arg_min=0, arg_max=2*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.trohoidAction, SIGNAL("activated()"), lambda func=curives.trohoid, arg_min=-20*pi, arg_max=20*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.evolventAction, SIGNAL("activated()"), lambda func=curives.evolvent, arg_min=0, arg_max=20*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.epitrohoidAction, SIGNAL("activated()"), lambda func=curives.epitrohoid, arg_min=-5*pi, arg_max=5*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.reducedEpitrohoidAction, SIGNAL("activated()"), lambda func=curives.reduced_epitrohoid, arg_min=-5*pi, arg_max=5*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.epicycloidAction, SIGNAL("activated()"), lambda func=curives.epicycloid, arg_min=0, arg_max=20*pi: self.set_curive_slot(func, arg_min, arg_max))
        self.connect(self.ui.pascalSnailAction, SIGNAL("activated()"), lambda func=curives.pascal_snail, arg_min=0, arg_max=2*pi: self.set_curive_slot(func, arg_min, arg_max))
    
        self.connect(self.ui.intervalOk, SIGNAL("clicked()"), self.change_interval_slot)
        self.connect(self.ui.scaleApply, SIGNAL("clicked()"), self.change_scale_slot)
        self.connect(self.ui.scaleReset, SIGNAL("clicked()"), self.scale_reset_slot)

    def reset_scale(self):
        self.ui.scaleX.setValue(1)
        self.ui.scaleY.setValue(1)
        self.plot.set_scale_x(1)
        self.plot.set_scale_y(1)
    
    def set_arg_min(self, value):
        self.plot.set_arg_min(value)
        self.ui.intervalMin.setValue(value)
    
    def set_arg_max(self, value):
        self.plot.set_arg_max(value)
        self.ui.intervalMax.setValue(value)
    
    #===================================Слоты====================================
    def set_curive_slot(self, func, arg_min=-1, arg_max=1, curive_name='', kwarg=[]):
        self.set_arg_min(arg_min)
        self.set_arg_max(arg_max)
        self.reset_scale()
        self.plot.set_line_function(func)
        self.plot.draw_plot()
    
    def change_scale_slot(self):
        self.plot.set_scale_x(self.ui.scaleX.value())
        self.plot.set_scale_y(self.ui.scaleY.value())
        self.plot.draw_plot();
    
    def scale_reset_slot(self):
        self.reset_scale()
        self.plot.draw_plot()
    
    def change_interval_slot(self):
        self.set_arg_min(self.ui.intervalMin.value())
        self.set_arg_max(self.ui.intervalMax.value())
        self.plot.draw_plot()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    PlotBuilder = PlotBuildApplication()
    PlotBuilder.show()
    sys.exit(app.exec_())