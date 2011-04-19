# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore
from QtCore import SIGNAL

from numpy import arange
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotCanvas(FigureCanvas):
    def __init__(self, axes_limits=(-10,-10,10,10), scale=(1.0,1.0), parent=None):
        fig = Figure(facecolor="white")
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.scale = scale
        self.grid  = True
        
        self.min_axis_x = axes_limits[0]
        self.min_axis_y = axes_limits[1]
        self.max_axis_x = axes_limits[2]
        self.max_axis_y = axes_limits[3]
        
        self.min_xticks = self.min_axis_x
        self.min_yticks = self.min_axis_y
        self.max_xticks = self.max_axis_x 
        self.max_yticks = self.max_axis_y
        
        self.axes = fig.add_subplot(111)
        self.figure.subplots_adjust(left=0.05, top=0.9, right=0.98, bottom=0.08)

        self.lines = {}

        self.draw_plot_area()

    def add_line(self, name, color):
        self.lines[name] = {'x':[], 'y':[], 'name':name, 'color':color}
        line_plot, = self.plot(self.lines[name], is_animated=True)
        self.lines[name]['line_plot'] = line_plot
        
    def save_plot(self, path):
        self.figure.canvas.print_figure(path)    
        
    def plot(self, line, is_animated=False):
        return self.axes.plot([self.scale[0]*x for x in line['x']], 
                              [self.scale[1]*y for y in line['y']],
                              linestyle='None', alpha=1, antialiased=False,
                              marker=',', mew=0.5, color=line['color'], ms=1.5, 
                              animated=is_animated, label=line['name'])

    def drop_points(self):
        for line in self.lines.values():
            line['x'] = []
            line['y'] = []

    def add_point(self, name, coords):
        self.lines[name]['x'].append(self.scale[0]*coords[0])
        self.lines[name]['y'].append(self.scale[1]*coords[1])
        
    def clear_plot_clear(self):
        self.axes.clear()
        
    def draw_static(self):    
        self.draw_plot_area()
        
        for name, line in self.lines.items():
            self.plot(line)
                       
        self.draw()
            
    def draw_animated(self, is_animated=True):
        self.restore_region(self.background)
        for name, line in self.lines.items():
            line['line_plot'].set_xdata(line['x'])
            line['line_plot'].set_ydata(line['y'])
            self.axes.draw_artist(line['line_plot'])
        
        self.blit(self.axes.bbox)
        
    def draw_plot_area(self):     
        self.axes.clear()          
        self.axes.set_title("X:%.2f   Y:%.2f" % self.scale)
        self.axes.set_xticks(arange(self.min_xticks,self.max_xticks,1))
        self.axes.set_yticks(arange(self.min_yticks,self.max_yticks,1))
            
        self.axes.set_xlim(self.min_axis_x, self.max_axis_x)
        self.axes.set_ylim(self.min_axis_y, self.max_axis_y)
        self.axes.grid(self.grid)
    
        for label in self.axes.xaxis.get_ticklabels():
            label.set_fontsize(8)
        for label in self.axes.yaxis.get_ticklabels():
            label.set_fontsize(8)
    
        self.axes.plot([self.min_axis_x - 1, self.max_axis_x + 1], [0, 0], color="black")
        self.axes.plot([0, 0], [self.min_axis_y - 1, self.max_axis_y + 1], color="black")
        
        for name, plot in self.lines.items():
            self.axes.plot(plot['x'], plot['y'],  plot['color'], label=name)
        
        if len(self.lines) != 0:
            self.axes.legend()    
        
        self.draw()    
        self.background = self.copy_from_bbox(self.axes.bbox)



class Pendulum(PlotCanvas):
    def __init__(self, title='', axes_limits=(-10,-10,10,10), scale=(1.0,1.0), parent=None):
        PlotCanvas.__init__(self, axes_limits, scale, parent)
        pos = 0
        self.pos = pos
        self.thread, = self.axes.plot([0, 0], [self.max_axis_y, pos], 'r-', linewidth=2)
        self.link,   = self.axes.plot([0], [pos], 'ro', linewidth=2)
        self.weight, = self.axes.plot([-1, 1, 1, -1, -1], [pos-1, pos-1, pos+1, pos+1, pos-1], 'ko-', linewidth=3) 
        
    def draw_plot_area(self):
        self.axes.set_title(u"Маятник")
        self.axes.set_xlim(self.min_axis_x, self.max_axis_x)
        self.axes.set_ylim(self.min_axis_y, self.max_axis_y)
        self.axes.plot([self.min_axis_x - 1, self.max_axis_x + 1], [0, 0], color="black")
        self.axes.plot([0, 0], [self.min_axis_y - 1, self.max_axis_y + 1], color="black")
        self.draw()
        self.background = self.copy_from_bbox(self.axes.bbox)

    def draw_animated(self):
        pos = self.pos
        self.thread.set_ydata([self.max_axis_y, pos])
        self.link.set_ydata([pos])
        self.weight.set_ydata([pos-1, pos-1, pos+1, pos+1, pos-1])

        self.restore_region(self.background)
        self.axes.draw_artist(self.thread)
        self.axes.draw_artist(self.link)
        self.axes.draw_artist(self.weight)
        self.blit(self.axes.bbox)
                
    def set_pos(self, value):
        self.pos = value*self.scale[1]
                
    def draw_static(self):    
        self.axes.clear()
        self.draw_plot_area()
        pos = self.pos * self.scale[0]
        self.axes.plot([0, 0], [self.max_axis_y, pos], 'r-', linewidth=2)
        self.axes.plot([0], [pos], 'ro', linewidth=2)
        self.axes.plot([-1, 1, 1, -1, -1], [pos-1, pos-1, pos+1, pos+1, pos-1], 'ko-', linewidth=3)
        self.draw()



class Oscillator(QtGui.QWidget):
    def __init__(self, parent=None):  
        QtGui.QWidget.__init__(self, parent)   
        self.setParent(parent)           
        
        self.scale_x = 1
        self.scale_y = 1
        self.time_limit = 20
        self.time_speed = 1
        self.integr_step = 0.01
        self.k = 0.005
        self.m = 0.05    
        self.omega = self.k/self.m
        self.current_time = 0
        self.timer = QtCore.QTimer()

        h_layout = QtGui.QHBoxLayout()
        v_layout = QtGui.QVBoxLayout()
        
        self.connect(self.timer, SIGNAL('timeout()'), self.timer_slot)
        
        self.plots = {}
        self.plots['wave']     = PlotCanvas(axes_limits=(-1, -5, 50, 5), scale=(self.scale_x, self.scale_y))
        self.plots['circle']   = PlotCanvas(axes_limits=(-15, -6, 15, 6),  scale=(self.scale_x, self.scale_y))
        self.plots['pendulum'] =   Pendulum(axes_limits=(-10, -5, 10, 5),  scale=(self.scale_x, self.scale_y))

        self.plots['wave'].figure.subplots_adjust(left=0.025, right=0.99)

        self.plots['wave'].add_line('x(t)','g')
        self.plots['wave'].add_line('v(t)','r')
        self.plots['wave'].add_line('dH(t)', 'b')
        self.plots['wave'].add_line('eiler_dH(t)', 'k')
        self.plots['circle'].add_line('v(x)','b')
        self.plots['circle'].add_line('eiler_v(x)', 'k')
        
        h_layout.addWidget(self.plots['circle'])
        h_layout.addWidget(self.plots['pendulum'])
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.plots['wave'])
        
        self.setLayout(v_layout)

    def set_scale_x(self, value):
        self.scale_x = value
        self.update_scale()

    def set_scale_y(self, value):
        self.scale_y = value
        self.update_scale()

    def update_scale(self):
        for plot in self.plots.values():
            plot.scale = (self.scale_x, self.scale_y)

    def set_grid(self, value):
        for plot in self.plots.values():
            plot.grid = value

    def set_time_limit(self, value):
        self.time_limit = value

    def set_integr_step(self, value):
        self.integr_step = value

    def set_k(self, value):
        self.k = value
        self.omega = self.k/self.m
        
    def set_m(self, value):
        self.m = value
        self.omega = self.k/self.m
        
    def clear_plots(self):       
        self.current_time = 0
        self.x = 0
        self.v = 1
        self.hv = (self.v**2)/2.0 + self.omega*(self.x**2) 
        self.h = 0
        self.eiler_x = 0
        self.eiler_v = 1
        self.eiler_hv = (self.eiler_v**2)/2.0 + self.omega*(self.eiler_x**2)
        self.eiler_h = 0
        for plot in self.plots.values():
            plot.drop_points()
            plot.clear_plot_clear()
            plot.draw_plot_area()  
        
    def calculate_values(self): 
        self.v = self.v - (self.omega*self.x*self.integr_step)
        self.x = self.x + (self.v*self.integr_step)
        hv = (self.v**2)/2.0 + self.omega*(self.x**2)
        self.h = (self.hv - hv)/self.hv
        self.hv = hv
        
        eiler_v = self.eiler_v
        self.eiler_v = self.eiler_v - (self.omega*self.eiler_x*self.integr_step)
        self.eiler_x = self.eiler_x + (eiler_v*self.integr_step) 
        eiler_hv = (self.eiler_v**2)/2.0 + self.omega*(self.eiler_x**2)
        self.eiler_h = (self.eiler_hv - eiler_hv)/self.eiler_hv
        self.eiler_hv = eiler_hv

    def append_points(self):
        self.plots['wave'].add_point('x(t)',   (self.t, self.x))
        self.plots['wave'].add_point('v(t)',   (self.t, self.v))
        self.plots['wave'].add_point('dH(t)',  (self.t, self.h))
        self.plots['wave'].add_point('eiler_dH(t)', (self.t, self.eiler_h))
        self.plots['circle'].add_point('v(x)', (self.x, self.v))
        self.plots['circle'].add_point('eiler_v(x)', (self.eiler_x, self.eiler_v))
        self.plots['pendulum'].set_pos(self.x)

    def save_plots(self, path):
        self.clear_plots()

        for t in arange(0, self.time_limit+self.integr_step, self.integr_step):
            self.t = t           
            self.append_points()
            self.calculate_values()
            
        for plot in self.plots.values():
            plot.draw_static()

        for name, plot in self.plots.items():
            plot.save_plot('%s/%s.png' % (path, name))

    def start_animated_draw(self):        
        self.clear_plots()       
        self.timer.start(1)       
        
    def timer_slot(self):
        if self.current_time < self.time_limit:            
            for t in arange(self.current_time, self.current_time+self.time_speed, self.integr_step):
                self.t = t
                self.append_points()
                self.calculate_values()
            
            for plot in self.plots.values():
                plot.draw_animated()

            self.current_time += self.time_speed
        else:
            self.timer.stop()