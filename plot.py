# -*- coding: utf8 -*-

from PyQt4 import QtGui

from numpy import arange, pi, abs
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

#Холст плоского графика
class PlotCanvas(FigureCanvas):
    #Конструктор
    def __init__(self, parent=None):              
        self.min_axis_x = -10
        self.max_axis_x = 10
        self.min_axis_y = -10
        self.max_axis_y = 10
        
        self.figure = Figure(figsize=(100, 100), facecolor="white")
        self.axes_freq = self.figure.add_subplot(121)
        self.axes_x_v =  self.figure.add_subplot(122)
        self.figure.subplots_adjust(left=0.05, right=0.96, wspace=0.15)
        
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)

    #Изменение масштаба
    def set_scale_x(self, value):
        self.scale_x = value

    def set_scale_y(self, value):
        self.scale_y = value

    #Изменение границ области определения аргумента
    def set_time_limit(self, value):
        self.time_limit = value

    def set_accuracy(self, value):
        self.accuracy = value

    def set_k(self, value):
        self.k = value
        
    def set_m(self, value):
        self.m = value

    #Отрисовка фигуры (не отображение)
    def draw_plot(self):
        self.axes_freq.clear()
        self.axes_x_v.clear()
    
        self.axes_freq.set_title("X: 1:%.1f   Y: 1:%.1f" % (self.scale_x, self.scale_y))
        self.axes_freq.set_xticks(arange(-100,100,1))
        self.axes_freq.set_yticks(arange(-100,100,1))
        self.axes_x_v.set_title("X: 1:%.1f   Y: 1:%.1f" % (self.scale_x, self.scale_y))
        self.axes_x_v.set_xticks(arange(-100,100,1))
        self.axes_x_v.set_yticks(arange(-100,100,1))
            
        self.axes_freq.set_xlim(-1, 19)
        self.axes_freq.set_ylim(self.min_axis_y, self.max_axis_y)
        self.axes_freq.grid(True)
        self.axes_x_v.set_xlim(self.min_axis_x, self.max_axis_x)
        self.axes_x_v.set_ylim(self.min_axis_y, self.max_axis_y)
        self.axes_x_v.grid(True)
    
        for label in self.axes_freq.xaxis.get_ticklabels():
            label.set_fontsize(8)
        for label in self.axes_freq.yaxis.get_ticklabels():
            label.set_fontsize(8)
        for label in self.axes_x_v.xaxis.get_ticklabels():
            label.set_fontsize(8)
        for label in self.axes_x_v.yaxis.get_ticklabels():
            label.set_fontsize(8)
    
        time = arange(0, self.time_limit, self.accuracy)
        v    = [1]
        x    = [0]
        
        omega = self.k/self.m
        
        for i in range(1, len(time)):
            v.append(v[-1] - (omega*x[-1])*self.accuracy)
            x.append(x[-1] + (v[-1]*self.accuracy))

        time = time*self.scale_x
        x = [x*self.scale_y for x in x]
        v = [v*self.scale_y for v in v]

        self.axes_freq.plot(time, x, 'r--', label='x(t)')
        self.axes_freq.plot(time, v, color="green", label='v(t)')
        self.axes_x_v.plot(x, v, color="blue", label='v(x)')
        
        self.axes_freq.legend()
        self.axes_x_v.legend()
        
        #Рисуем кресты осей
        self.axes_freq.plot([-10, self.time_limit], [0, 0], color="black")
        self.axes_freq.plot([0, 0], [-10, 10], color="black")
        self.axes_x_v.plot([-10, 10], [0, 0], color="black")
        self.axes_x_v.plot([0, 0], [-10, 10], color="black")
        self.draw()