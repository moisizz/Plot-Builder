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
        FigureCanvas.__init__(self, Figure(figsize=(100, 100), facecolor="white"))   
        self.setParent(parent)           
        self.min_axis_x = -5
        self.max_axis_x = 10
        self.min_axis_y = -10
        self.max_axis_y = 10
        
        self.scale_x = 1
        self.scale_y = 1
        self.time_limit = 20
        self.integr_step = 0.01
        self.k = 0.005
        self.m = 0.05    
        
        self.plots = {}
        self.plots['x(t)v(t)'] = self.figure.add_subplot(121)
        self.plots['v(x)'] = self.figure.add_subplot(122) 
        
        self.figure.subplots_adjust(left=0.05, right=0.96, wspace=0.15)        
        self.draw_plot_area()
        for axes in self.plots.values():
            axes.back = self.copy_from_bbox(axes.bbox)
        
        time = arange(0, self.time_limit, self.integr_step)
        
        self.current_time = 0
        

    #Изменение масштаба
    def set_scale_x(self, value):
        self.scale_x = value

    def set_scale_y(self, value):
        self.scale_y = value

    #Изменение границ области определения аргумента
    def set_time_limit(self, value):
        self.time_limit = value

    def set_integr_step(self, value):
        self.integr_step = value

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

            axes.plot([-10, 10], [0, 0], color="black")
            axes.plot([0, 0], [-10, 10], color="black")
            
        
    #Отрисовка фигуры (не отображение)
    def draw_plot(self):        
        self.current_time = 0
        self.startTimer(self.time_limit)
        
    def timerEvent(self, evt):
        if self.current_time < self.time_limit:
            self.current_time += 0.5
                
            for axes in self.plots.values():    
                self.figure.canvas.restore_region(axes.back)
    
            time = arange(0, self.current_time, self.integr_step)
            v    = [1]
            x    = [0]
            
            omega = self.k/self.m
            
            for i in range(1, len(time)):
                v.append(v[-1] - (omega*x[-1])*self.integr_step)
                x.append(x[-1] + (v[-1]*self.integr_step))
            
            time = time*self.scale_x
            x = [x*self.scale_y for x in x]
            v = [v*self.scale_y for v in v]
            
            x_line, = self.plots['x(t)v(t)'].plot(time,x, 'r--', animated=True, label='x(t)')
            v_line, = self.plots['x(t)v(t)'].plot(time,v, animated=True, color="green", label='v(t)')
            x_v_line, = self.plots['v(x)'].plot(x,v, animated=True, color="blue", label='v(x)')
            
            self.plots['x(t)v(t)'].draw_artist(x_line)
            self.plots['x(t)v(t)'].draw_artist(v_line)
            self.plots['v(x)'].draw_artist(x_v_line)

            for axes in self.plots.values():
                self.figure.canvas.blit(axes.bbox)