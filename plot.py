# -*- coding: utf8 -*-

from PyQt4 import QtGui

from numpy import arange, pi, abs
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import time

class PlotCanvas(FigureCanvas):
    def __init__(self, axes_limits=(-10,-10,10,10), scale=(1.0,1.0), parent=None):
        fig = Figure(facecolor="white")
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.scale = scale
        
        self.min_axis_x = axes_limits[0]
        self.min_axis_y = axes_limits[1]
        self.max_axis_x = axes_limits[2]
        self.max_axis_y = axes_limits[3]
        
        self.min_xticks = self.min_axis_x
        self.min_yticks = self.min_axis_y
        self.max_xticks = self.max_axis_x 
        self.max_yticks = self.max_axis_y
        
        self.axes = fig.add_subplot(111)
        self.figure.subplots_adjust(left=0.05, top=0.9, right=0.98, bottom=0.05)

        self.lines = {}

        self.draw_plot_area()
    
    #Сохранение картинки графика
    def save_plot(self, path):
        self.figure.canvas.print_figure(path)
        
    #Очистка для статичного отображения
    def static_clear(self):
        self.axes.clear()
        
    #Очистка для анимированного отображения
    def animated_clear(self):
        self.draw()
        
    def draw_static(self):    
        self.draw_plot_area()
        
        for name, plot in self.lines.items():
            self.axes.plot([self.scale[0]*x for x in plot['x']], 
                           [self.scale[1]*y for y in plot['y']], 
                           plot['line_type'], label=name, linewidth=0.8)
        self.draw()
            
    def draw_animated(self):
        self.restore_region(self.background)
        for name, plot in self.lines.items():
            line, = self.axes.plot([self.scale[0]*x for x in plot['x']], 
                                   [self.scale[1]*y for y in plot['y']], 
                                   plot['line_type'], 
                                   animated=True, label=name, linewidth=0.8)
            self.axes.draw_artist(line)
            self.blit(self.axes.bbox)
        
    #Отрисовка плоскостей
    def draw_plot_area(self):     
        self.axes.clear()          
        self.axes.set_title("X:%.2f   Y:%.2f" % self.scale)
        self.axes.set_xticks(arange(self.min_xticks,self.max_xticks,1))
        self.axes.set_yticks(arange(self.min_yticks,self.max_yticks,1))
            
        self.axes.set_xlim(self.min_axis_x, self.max_axis_x)
        self.axes.set_ylim(self.min_axis_y, self.max_axis_y)
        self.axes.grid(True)
    
        for label in self.axes.xaxis.get_ticklabels():
            label.set_fontsize(8)
        for label in self.axes.yaxis.get_ticklabels():
            label.set_fontsize(8)
    
        self.axes.plot([self.min_axis_x - 1, self.max_axis_x + 1], [0, 0], color="black")
        self.axes.plot([0, 0], [self.min_axis_y - 1, self.max_axis_y + 1], color="black")
        
        for name, plot in self.lines.items():
            self.axes.plot(plot['x'], plot['y'], plot['line_type'], label=name)
        
        if len(self.lines) != 0:
            self.axes.legend()    
        
        self.draw()    
        self.background = self.copy_from_bbox(self.axes.bbox)


class Pendulum(PlotCanvas):
    def __init__(self, title='', axes_limits=(-10,-10,10,10), scale=(1.0,1.0), parent=None):
        PlotCanvas.__init__(self, axes_limits, scale, parent)
        self.pos = 0
        
    def draw_plot_area(self):
        self.axes.set_title(u"Маятник")
        self.axes.set_xlim(self.min_axis_x, self.max_axis_x)
        self.axes.set_ylim(self.min_axis_y, self.max_axis_y)
        self.axes.plot([self.min_axis_x - 1, self.max_axis_x + 1], [0, 0], color="black")
        self.axes.plot([0, 0], [self.min_axis_y - 1, self.max_axis_y + 1], color="black")

    def draw_animated(self):
        self.draw_static()
                
    def set_pos(self, value):
        self.pos = value
                
    def draw_static(self):    
        self.axes.clear()
        self.draw_plot_area()
        pos = self.pos * self.scale[0]
        self.axes.plot([0, 0], [self.max_axis_y, pos], 'r-', linewidth=2)
        self.axes.plot([0], [pos], 'ro', linewidth=2)
        self.axes.plot([-1, 1, 1, -1, -1], [pos-1, pos-1, pos+1, pos+1, pos-1], 'r-')
        self.draw()

#Осциллятор
class Oscillator(QtGui.QWidget):
    #Конструктор
    def __init__(self, parent=None):  
        QtGui.QWidget.__init__(self, parent)   
        self.setParent(parent)           
        
        self.scale_x = 1
        self.scale_y = 1
        self.time_limit = 20
        self.integr_step = 0.2
        self.k = 0.005
        self.m = 0.05    

        h_layout = QtGui.QHBoxLayout()
        v_layout = QtGui.QVBoxLayout()
        
        self.plots = {}
        self.plots['wave']     = PlotCanvas(axes_limits=(-1, -5, 25, 5), scale=(self.scale_x, self.scale_y))
        self.plots['wave'].lines['x(t)'] = {'x':[], 'y':[], 'line_type':'g-'}
        self.plots['wave'].lines['v(t)'] = {'x':[], 'y':[], 'line_type':'r--'}
        self.plots['circle']   = PlotCanvas(axes_limits=(-8, -6, 8, 6), scale=(self.scale_x, self.scale_y))
        self.plots['circle'].lines['v(x)'] = {'x':[], 'y':[], 'line_type':'b-'}
        self.plots['pendulum'] = Pendulum(axes_limits=(-5, -5, 5, 5), scale=(self.scale_x, self.scale_y))
        
        h_layout.addWidget(self.plots['circle'])
        h_layout.addWidget(self.plots['pendulum'])
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.plots['wave'])
        
        self.setLayout(v_layout)
        self.current_time = 0

    #Изменение масштаба
    def set_scale_x(self, value):
        self.scale_x = value
        self.update_scale()

    def set_scale_y(self, value):
        self.scale_y = value
        self.update_scale()

    def update_scale(self):
        for plot in self.plots.values():
            plot.scale = (self.scale_x, self.scale_y)

    #Изменение границ области определения аргумента
    def set_time_limit(self, value):
        self.time_limit = value

    def set_integr_step(self, value):
        self.integr_step = value

    def set_k(self, value):
        self.k = value
        
    def set_m(self, value):
        self.m = value

    #Сохранить графики
    def save_plots(self, path):
        t_values = []
        x_values = []
        v_values = []
        
        x = 0
        v = 1

        for t in arange(0, self.time_limit+self.integr_step, self.integr_step):
            t_values.append(t)
            x_values.append(x)
            v_values.append(v)            
            (x, v) = self.calculate_values(x, v)
            
        self.plots['wave'].lines['x(t)']['x']   = t_values
        self.plots['wave'].lines['x(t)']['y']   = x_values
        self.plots['wave'].lines['v(t)']['x']   = t_values
        self.plots['wave'].lines['v(t)']['y']   = v_values
        self.plots['circle'].lines['v(x)']['x'] = x_values
        self.plots['circle'].lines['v(x)']['y'] = v_values
        self.plots['pendulum'].set_pos(x_values[-1])
    
        for plot in self.plots.values():
            plot.draw_static()

        for name, plot in self.plots.items():
            plot.save_plot('%s/%s.png' % (path, name))

    #Начать анимированную отрисовку графиков
    def start_animated_draw(self):        
        self.current_time = 0
        for axes in self.plots.values():
            axes.animated_clear()
            
        self.x = 0
        self.v = 1

        self.plots['wave'].lines['x(t)']['x'] = [self.current_time]
        self.plots['wave'].lines['x(t)']['y'] = [self.x]
        self.plots['wave'].lines['v(t)']['x'] = [self.current_time]
        self.plots['wave'].lines['v(t)']['y'] = [self.v]
        self.plots['circle'].lines['v(x)']['x'] = [self.x]
        self.plots['circle'].lines['v(x)']['y'] = [self.v]
        
        for plot in self.plots.values():
            plot.draw_plot_area()
        
        self.startTimer(1)       
        
    #Расчет необходимых значений
    def calculate_values(self, x, v):   
        omega = self.k/self.m
        
        new_v = v - (omega*x*self.integr_step)
        new_x = x + (new_v*self.integr_step)

        return (new_x, new_v)
        
    #Событие таймера, рисующ
    def timerEvent(self, evt):
        if self.current_time <= self.time_limit:            
            self.plots['wave'].lines['x(t)']['x'].append(self.current_time)
            self.plots['wave'].lines['x(t)']['y'].append(self.x)
            self.plots['wave'].lines['v(t)']['x'].append(self.current_time)
            self.plots['wave'].lines['v(t)']['y'].append(self.v)
            self.plots['circle'].lines['v(x)']['x'].append(self.x)
            self.plots['circle'].lines['v(x)']['y'].append(self.v)
            self.plots['pendulum'].set_pos(self.x)
            
            for plot in self.plots.values():
                plot.draw_animated()
                
            self.current_time += self.integr_step
            
            (self.x, self.v) = self.calculate_values(self.x, self.v)