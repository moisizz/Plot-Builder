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
        self.draw_type = 'points'
        
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

    def add_line(self, name, x_name, y_name, calc_name, color, is_enabled=True):
        line_key = "%s_%s_%s" % (calc_name, x_name, y_name)
        self.lines[line_key] = {'x':[], 'x_name':x_name, 'y':[], 'y_name':y_name, 'calc_name':calc_name, 
                                'name':name, 'color':color, 'enabled':is_enabled}
        line_plot, = self.plot(self.lines[line_key], is_animated=True)
        self.lines[line_key]['line_plot'] = line_plot
        
    def save_plot(self, path):
        self.figure.canvas.print_figure(path)    
        
    def plot(self, line, is_animated=False):
        if self.draw_type == 'points':
            linestyle='None'
            antialiased=False
            marker=','
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
        self.thread, = self.axes.plot([0, 0], [self.max_axis_y, pos], 'r-', linewidth=2)
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
        self.thread.set_ydata([self.max_axis_y, pos])
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
        
        self.scale_x = 1
        self.scale_y = 1
        self.time_limit = 42
        self.time_speed = 1
        self.integr_step = 0.1
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

        self.plots['wave'].add_line(u'Канон. x(t)', 't', 'x', 'canonical', 'g', True)
        self.plots['wave'].add_line(u'Канон. v(t)', 't', 'v', 'canonical', 'r', False)
        
        self.plots['wave'].add_line(u'Эйлер x(t)', 't', 'x', 'eiler', 'c', False)
        self.plots['wave'].add_line(u'Эйлер v(t)', 't', 'v', 'eiler', 'm', False)
        
        self.plots['wave'].add_line(u'ИККИ x(t)', 't', 'x', 'vxxv', 'y', True)
        self.plots['wave'].add_line(u'ИККИ v(t)', 't', 'v', 'vxxv', 'k', False)
        
        self.plots['wave'].add_line(u'Канон. dH(t)', 't', 'dh', 'canonical', 'b', False)
        self.plots['wave'].add_line(u'Эйлер dH(t)',  't', 'dh', 'eiler',  'k', False)
        self.plots['wave'].add_line(u'ИККИ dH(t)',   't', 'dh', 'vxxv',   'm', False)

        self.plots['circle'].add_line(u'Канон. v(x)', 'x', 'v', 'canonical', 'b', True)
        self.plots['circle'].add_line(u'Эйлер v(x)',  'x', 'v', 'eiler',    'k', False)
        self.plots['circle'].add_line(u'ИККИ v(x)',   'x', 'v', 'vxxv',    'r', True)
        
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

    def set_draw_type(self, type):
        for plot in self.plots.values():
            plot.set_draw_type(type)

    def switch_line(self, plot_name, line_name, state):
        self.plots[plot_name].lines[line_name]['enabled'] = state

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
        #Обнуляем время
        self.values = {}
        self.current_time = 0
        self.values['time'] = 0
        
        #Задаем начальные значения положения и скорости
        x = 0
        v = 1
        
        #------------------Канонический метод--------------------------
        self.values['canonical'] = {}
        self.values['canonical']['x'] = x
        self.values['canonical']['v'] = v
        self.values['canonical']['h0'] = (v**2)/2.0 + self.omega*(x**2) 
        self.values['canonical']['dh'] = self.values['canonical']['h0']
        
        #--------------------------Метод Эйлера------------------------
        self.values['eiler'] = {}
        self.values['eiler']['x'] = x
        self.values['eiler']['v'] = v
        self.values['eiler']['h0'] = (v**2)/2.0 + self.omega*(x**2)
        self.values['eiler']['dh'] = self.values['eiler']['h0']

        #------------------Импульс-координата-координата-импульс--------------------------
        self.values['vxxv'] = {}
        self.values['vxxv']['x'] = x
        self.values['vxxv']['v'] = v
        self.values['vxxv']['h0'] = (v**2)/2.0 + self.omega*(x**2) 
        self.values['vxxv']['dh'] = self.values['vxxv']['h0']
        
        for plot in self.plots.values():
            plot.drop_points()
            plot.clear_plot_clear()
            plot.draw_plot_area()  
        
    def calculate_values(self): 
        omega = self.omega
        tt = self.integr_step

        #============================Канонический метод=================================
        (v, x, h0)  = (self.values['canonical']['v'], self.values['canonical']['x'], self.values['canonical']['h0'])
        
        v  = v - (omega * x * tt)
        x  = x + (v * tt)
        h  = (v**2)/2.0 + omega*(x**2)
        dh = (h - h0)/h0
        
        (self.values['canonical']['v'], self.values['canonical']['x'], self.values['canonical']['dh']) = (v, x, dh) 
        
        #============================Метод Эйлера=================================
        (v, x, h0)  = (self.values['eiler']['v'], self.values['eiler']['x'], self.values['eiler']['h0'])
        
        old_v = v
        v  = v - (omega * x * tt)
        x  = x + (old_v * tt)
        h  = (v**2)/2.0 + omega*(x**2)
        dh = (h - h0)/h0
        
        (self.values['eiler']['v'], self.values['eiler']['x'], self.values['eiler']['dh']) = (v, x, dh) 
        
        #============================Импульс-координата-координата-импульс=================================
        (v, x, h0)  = (self.values['vxxv']['v'], self.values['vxxv']['x'], self.values['vxxv']['h0'])
        
        v  = v - (omega * x * tt)
        x  = x + (v * tt)
        x  = x + (v * tt)
        v  = v - (omega * x * tt)
        h  = (v**2)/2.0 + omega*(x**2)
        dh = (h - h0)/h0
        
        (self.values['vxxv']['v'], self.values['vxxv']['x'], self.values['vxxv']['dh']) = (v, x, dh) 

    def append_points(self):
        for name, plot in self.plots.items():
            if name != 'pendulum':
                for name, line in plot.lines.items():
                    calc_name = line['calc_name']
                    if line['x_name'] == 't':
                        x = self.values['t']
                    else:
                        x = self.values[calc_name][line['x_name']]
                        
                    if line['y_name'] == 't':
                        y = self.values['t']
                    else:
                        y = self.values[calc_name][line['y_name']]    
                    plot.add_point(name, (x, y))
        
        self.plots['pendulum'].set_pos(self.values['canonical']['x'])

    def save_plots(self, path):
        self.clear_plots()

        for t in arange(0, self.time_limit+self.integr_step, self.integr_step):
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
        if self.current_time < self.time_limit:            
            for t in arange(self.current_time, self.current_time+self.time_speed, self.integr_step):
                self.values['t'] = t
                self.append_points()
                self.calculate_values()
            
            for plot in self.plots.values():
                plot.draw_animated()

            self.current_time += self.time_speed
        else:
            self.timer.stop()