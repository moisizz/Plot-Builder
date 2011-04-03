# -*- coding: utf8 -*-

from numpy import *

def circle(t):
    x = sin(t)
    y = cos(t)
    return (x, y)

def cardioid(t):
    x = 2*cos(t)*(1+cos(t))
    y = 2*sin(t)*(1+cos(t))
    return (x, y)

def astroid(t):
    x = cos(t)**3
    y = sin(t)**3
    return (x, y)

def hypotrohoid(t):
    R = 10
    r = 1
    h = 9.3
    
    x = (R-r)*cos(t) + h*cos((R-r)*t/r)
    y = (R-r)*sin(t) - h*sin((R-r)*t/r)
    return (x, y)

def hypocycloid(t):
    r = 0.5
    k = 5.5
    
    x = r*(k-1)*(cos(t) + (cos(t*(k-1)))/(k-1))
    y = r*(k-1)*(sin(t) - (sin(t*(k-1)))/(k-1))
    return (x, y)

def deltoid(t):
    r = 1
    
    x = 2*r*cos(t) + r*cos(2*t)
    y = 2*r*sin(t) - r*sin(2*t)
    return (x, y)

def bern_leminiskate(t):
    c = 3
    
    x = c*sqrt(2)*(t + t**3)/(1 + t**4)
    y = c*sqrt(2)*(t - t**3)/(1 + t**4)
    return (x, y)

def jeron_leminiskate(t):
    x = (t**2 - 1)/(t**2 + 1)
    y = 2*t*(t**2 - 1)/(t**2 + 1)**2
    return (x, y)

def log_spiral(t):
    r = 3
    a = 0.8
    b = 0.3
  
    x = a*exp(b*t)*cos(t)
    y = a*exp(b*t)*sin(t)
    return (x, y)

def nefroid(t):
    r = 1
    
    x = 6*r*cos(t) - 4*r*cos(t)**3
    y = 4*r*sin(t)**3
    return (x, y)

def trohoid(t):
    r = 1
    h = 2
    
    x = r*t - h*sin(t)
    y = r   - h*cos(t)
    return (x, y)

def evolvent(t):
    x = 0.1*(cos(t) + t*sin(t))
    y = 0.1*(sin(t) - t*cos(t))
    return (x, y)

def epitrohoid(t):
    m = 0.2
    h = 0.3
    R = 1
    
    x = R*(m + 1)*cos(m*t) - h*cos(t*(m + 1))
    y = R*(m + 1)*sin(m*t) - h*sin(t*(m + 1))
    return (x, y)

def reduced_epitrohoid(t):
    m = 0.2
    h = 0.1
    R = 1
    
    x = R*(m + 1)*cos(m*t) - h*cos(t*(m + 1))
    y = R*(m + 1)*sin(m*t) - h*sin(t*(m + 1))
    return (x, y)

def pascal_snail(t):
    m = 1
    h = 1.5
    R = 1
    
    x = R*(m + 1)*cos(m*t) - h*cos(t*(m + 1))
    y = R*(m + 1)*sin(m*t) - h*sin(t*(m + 1))
    return (x, y)

def epicycloid(t):
    k = 2.1
    r = 1
    
    x = r*(k + 1)*(cos(t) - (cos((k + 1)*t))/(k + 1))
    y = r*(k + 1)*(sin(t) - (sin((k + 1)*t))/(k + 1))
    return (x, y)