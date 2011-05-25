# -*- coding: utf8 -*-

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import SIGNAL

from numpy import arange, sin, cos, sqrt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class PlotCanvas(FigureCanvas):
    def __init__(self, axes_limits=(-10,-10,10,10), scale=(1.0,1.0), parent=None):
        fig = Figure(facecolor="white")
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        self.scale = scale
        self.grid  = True
        self.draw_type = 'lines'
        
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

    def add_line(self, name, x_name, y_name, calc_name, color, is_enabled=True, marker=','):
        line_key = "%s_%s_%s" % (calc_name, x_name, y_name)
        self.lines[line_key] = {'x':[], 'x_name':x_name, 'y':[], 'y_name':y_name, 'calc_name':calc_name, 
                                'name':name, 'color':color, 'enabled':is_enabled, 'marker':marker}
        line_plot, = self.plot(self.lines[line_key], is_animated=True)
        self.lines[line_key]['line_plot'] = line_plot
        
    def save_plot(self, path):
        self.figure.canvas.print_figure(path)    
        
    def plot(self, line, is_animated=False):
        if self.draw_type == 'points':
            linestyle='None'
            antialiased=False
            marker=line['marker']
            mew=0.5
            ms=1.5
        elif self.draw_type == 'lines':
            linestyle='-'
            antialiased=True
            marker='None'
            mew=0
            ms=0

        return self.axes.plot([self.scale[0]*x for x in line['x']], 
                              [self.scale[1]*y for y in line['y']],
                              linestyle=linestyle, alpha=1, antialiased=antialiased,
                              marker=marker, mew=mew, color=line['color'], ms=ms, 
                              animated=is_animated, label=line['name'])

    def drop_points(self):
        for line in self.lines.values():
            line['x'] = []
            line['y'] = []

    def add_point(self, name, coords):
        if self.lines[name]['enabled']:
            self.lines[name]['x'].append(self.scale[0]*coords[0])
            self.lines[name]['y'].append(self.scale[1]*coords[1])
        
    def clear_plot_clear(self):
        self.axes.clear()
        
    def set_draw_type(self, type):
        self.draw_type = type
        
        for line in self.lines.values():
            line_plot, = self.plot(line, is_animated=True)
            line['line_plot'] = line_plot
        
    def draw_static(self):    
        self.draw_plot_area()
        
        for name, line in self.lines.items():
            if line['enabled']:
                self.plot(line)
                       
        self.draw()
            
    def draw_animated(self, is_animated=True):
        self.restore_region(self.background)
        for name, line in self.lines.items():
            if(line['enabled']):
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
        
        for name, line in self.lines.items():
            if(line['enabled']):
                self.axes.plot(line['x'], line['y'],  line['color'], label=line['name'])
        
        if len(self.lines) != 0:
            self.axes.legend()    
        
        self.draw()    
        self.background = self.copy_from_bbox(self.axes.bbox)

class Pendulum(PlotCanvas):
    def __init__(self, title='', axes_limits=(-10,-10,10,10), scale=(1.0,1.0), parent=None):
        PlotCanvas.__init__(self, axes_limits, scale, parent)
        pos = 0
        self.pos = pos
        self.weight_size = 40
        self.weight_edge_width = 3
        self.weight_type = 'o'
        self.weight_face_color = 'w'
        self.weight_edge_color = 'k'
        self.thread, = self.axes.plot([0, 0], [self.max_axis_y+5, pos], 'r-', linewidth=2)
        self.link,   = self.axes.plot([0], [pos], 'ks', lw=2, ms=self.weight_size,  
                                                              marker=self.weight_type,
                                                              mec=self.weight_edge_color, 
                                                              mfc=self.weight_face_color, 
                                                              mew=self.weight_edge_width)
        
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
        self.thread.set_ydata([self.max_axis_y+5, pos])
        self.link.set_ydata([pos])

        self.restore_region(self.background)
        self.axes.draw_artist(self.thread)
        self.axes.draw_artist(self.link)
        self.blit(self.axes.bbox)
                
    def set_pos(self, value):
        self.pos = value*self.scale[1]
                
    def draw_static(self):    
        self.axes.clear()
        self.draw_plot_area()
        pos = self.pos * self.scale[0]
        self.axes.plot([0, 0], [self.max_axis_y, pos], 'r-', linewidth=2)
        self.axes.plot([0], [pos], 'r', lw=2, ms=self.weight_size, 
                                              marker=self.weight_type,
                                              mec=self.weight_edge_color, 
                                              mfc=self.weight_face_color, 
                                              mew=self.weight_edge_width)
        self.draw()

class Oscillator(QtGui.QWidget):
    def __init__(self, parent=None):  
        QtGui.QWidget.__init__(self, parent)   
        self.setParent(parent)           
        
        self.init_default_params()
        self.timer = QtCore.QTimer()

        h_layout = QtGui.QHBoxLayout()
        v_layout = QtGui.QVBoxLayout()
        
        self.connect(self.timer, SIGNAL('timeout()'), self.timer_slot)
        
        self.plots = {}
        self.plots['wave']     = PlotCanvas(axes_limits=(-1, -5, 50, 5), scale=(self.scale_x, self.scale_y))
        self.plots['circle']   = PlotCanvas(axes_limits=(-15, -6, 15, 6),  scale=(self.scale_x, self.scale_y))
        self.plots['pendulum'] =   Pendulum(axes_limits=(-10, -5, 10, 5),  scale=(self.scale_x, self.scale_y))

        self.plots['wave'].figure.subplots_adjust(left=0.025, right=0.99)

        self.plots['wave'].add_line(u'Канон. x(t)',   't', 'x',  'canonical', 'r', True)
        self.plots['wave'].add_line(u'Канон. v(t)',   't', 'v',  'canonical', 'g', True)
        self.plots['circle'].add_line(u'Канон. v(x)', 'x', 'v',  'canonical', 'c', True)
        
        h_layout.addWidget(self.plots['circle'])
        h_layout.addWidget(self.plots['pendulum'])
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.plots['wave'])
        
        self.setLayout(v_layout)

    def init_default_params(self):
        self.scale_x = 1
        self.scale_y = 1
        self.time_speed = 1

        self.params = {}

        self.params['time_limit'] = 42
        self.params['integr_step'] = 0.1
        self.params['k'] = 0.005
        self.params['m'] = 0.05
        self.params['f'] = 0
        self.params['f_omega'] = 0
        self.params['resist_koef'] = 0
        self.params['v'] = 1
        self.params['x'] = 0
        
        self.current_time = 0

    def set_scale_x(self, value):
        self.scale_x = value
        self.update_scale()

    def set_scale_y(self, value):
        self.scale_y = value
        self.update_scale()

    def update_scale(self):
        for plot in self.plots.values():
            plot.scale = (self.scale_x, self.scale_y)

    def set_draw_type(self, type):
        for plot in self.plots.values():
            plot.set_draw_type(type)
            
    def set_grid(self, value):
        for plot in self.plots.values():
            plot.grid = value

    def set_time_limit(self, value):
        self.time_limit = value

    def clear_plots(self):   
        #Обнуляем время
        self.values = {}
        self.current_time = 0
        self.values['t'] = 0
        
        #Задаем начальные значения положения и скорости
        x = self.params['x']
        v = self.params['v']
        
        self.values['methods'] = {}
        self.values['methods']['canonical'] = {}
        
        for method in self.values['methods'].keys():
            self.values['methods'][method]['x'] = x
            self.values['methods'][method]['v'] = v
        
        for plot in self.plots.values():
            plot.drop_points()
            plot.clear_plot_clear()
            plot.draw_plot_area()  
        
    def calculate_values(self): 
        omega2 = self.params['k']/self.params['m']
        tt = self.params['integr_step']
        resist_koef = self.params['resist_koef']
        F = self.params['f']
        f_omega = self.params['f_omega']
        t = self.values['t']
        mass = self.params['m']
        values = self.values['methods']['canonical']


        (v, x)  = (values['v'], values['x'])
               
        v = v - (omega2 * x * tt) - resist_koef*v*tt + (F/mass)*cos(f_omega*t)*tt
        x = x + (v * tt)
        
        (values['v'], values['x']) = (v, x) 

    def append_points(self):
        for name, plot in self.plots.items():
            if name != 'pendulum':
                for name, line in plot.lines.items():
                    calc_name = line['calc_name']
                    if line['x_name'] == 't':
                        x = self.values['t']
                    else:
                        x = self.values['methods'][calc_name][line['x_name']]
                        
                    if line['y_name'] == 't':
                        y = self.values['t']
                    else:
                        y = self.values['methods'][calc_name][line['y_name']]    
                    plot.add_point(name, (x, y))
        
        self.plots['pendulum'].set_pos(self.values['methods']['canonical']['x'])

    def save_plots(self, path):
        self.clear_plots()

        for t in arange(0, self.params['time_limit']+self.params['integr_step'], self.params['integr_step']):
            self.values['t'] = t           
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
        if self.current_time < self.params['time_limit']:            
            for t in arange(self.current_time, self.current_time+self.time_speed, self.params['integr_step']):
                self.calculate_values()
                self.values['t'] = t
                self.append_points()
            
            for plot in self.plots.values():
                plot.draw_animated()

            self.current_time += self.time_speed
        else:
            self.timer.stop()