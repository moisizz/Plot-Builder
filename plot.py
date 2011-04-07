# -*- coding: utf8 -*-

from PyQt4 import QtGui

from numpy import arange, pi, abs
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import time

#Холст плоского графика
class PlotCanvas(FigureCanvas):
    #Конструктор
    def __init__(self, parent=None):              
        self.min_axis_x = -10
        self.max_axis_x = 10
        self.min_axis_y = -10
        self.max_axis_y = 10
        
        self.figure = Figure(figsize=(100, 100), facecolor="white")
        self.plots = {}
        self.plots['x(t)v(t)'] = self.figure.add_subplot(121)
        self.plots['v(x)'] = self.figure.add_subplot(122) 

        self.figure.subplots_adjust(left=0.05, right=0.96, wspace=0.15)
        
        FigureCanvas.__init__(self, self.figure)
        self.setParent(parent)            
        
        self.current_time = 0

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

    #Отрисовка плоскостей
    def draw_plot_area(self):
        for axes in self.plots.values():
            axes.set_title("X: 1:%.1f   Y: 1:%.1f" % (self.scale_x, self.scale_y))
            axes.set_xticks(arange(-40,40,1))
            axes.set_yticks(arange(-40,40,1))
                
            axes.set_xlim(self.min_axis_x, self.max_axis_x)
            axes.set_ylim(self.min_axis_y, self.max_axis_y)
            axes.grid(True)
        
            for label in axes.xaxis.get_ticklabels():
                label.set_fontsize(8)
            for label in axes.yaxis.get_ticklabels():
                label.set_fontsize(8)

            axes.plot([-10, self.time_limit], [0, 0], color="black")
            axes.plot([0, 0], [-10, 10], color="black")
            
        
    #Отрисовка фигуры (не отображение)
    def draw_plot(self):
        for axes in self.plots.values():
            axes.clear()
        
        self.draw_plot_area()
    
        time = arange(0, self.current_time, self.accuracy)
        v    = [1]
        x    = [0]
        
        omega = self.k/self.m
        
        for i in range(1, len(time)):
            v.append(v[-1] - (omega*x[-1])*self.accuracy)
            x.append(x[-1] + (v[-1]*self.accuracy))

        time = time*self.scale_x
        x = [x*self.scale_y for x in x]
        v = [v*self.scale_y for v in v]

        self.plots['x(t)v(t)'].plot(time, x, 'r--', label='x(t)')
        self.plots['x(t)v(t)'].plot(time, v, color="green", label='v(t)')
        self.plots['v(x)'].plot(x, v, color="blue", label='v(x)')
        
        for axes in self.plots.values():
            axes.legend();

        self.draw()
        
    def timerEvent(self, evt):
        '''current_size = self.ax.bbox.width, self.ax.bbox.height
        if self.old_size != current_size:
            self.old_size = current_size
            self.ax.clear()
            self.ax.grid()
            self.draw()
            self.ax_background = self.copy_from_bbox(self.ax.bbox)'''

        if self.current_time != self.time_limit:
            self.current_time += 1
            
        self.draw_plot()