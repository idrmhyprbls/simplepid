#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""TBD"""
from __future__ import division, print_function

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from pid import PID

# Subplots
fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, bottom=0.35)

# Data
dt = 1/30.
t = np.arange(0.0, 20.0, dt)
kp_init = 0.03
ki_init = 0.06
kd_init = 0
max_int_init = 16
min_int_init = -16
max_out_init = .4
min_out_init = -.4
pid = PID(kp_init, ki_init, kd_init, dt, max_int_init, min_int_init, max_out_init, min_out_init)
pos = 0.
s = []
for frame in t:
    if frame == 0.:
        s.append(pos)
        continue
    pos += pid.compute(150, pos)
    s.append(pos)

# Plot
l, = plt.plot(t, s, '-', lw=2, color='red')

# Axis
plt.axis([0, 20, 0, 210])
axcolor = 'lightgoldenrodyellow'
kp = plt.axes([0.25, 0.25, 0.65, 0.03], axisbg=axcolor)
ki  = plt.axes([0.25, 0.2, 0.65, 0.03], axisbg=axcolor)
kd  = plt.axes([0.25, 0.15, 0.65, 0.03], axisbg=axcolor)
max_int = plt.axes([0.25, 0.10, 0.65, 0.03], axisbg=axcolor)
max_out = plt.axes([0.25, 0.05, 0.65, 0.03], axisbg=axcolor)

# Sliders
# skp = Slider(kp, 'Kp', 0, 2, valinit=kp_init)
# ski = Slider(ki, 'Ki', 0, 10, valinit=ki_init)
# skd = Slider(kd, 'Kd', 0, .05, valinit=kd_init)
# smi = Slider(max_int, 'MaxInt', 0, 2/dt, valinit=max_int_init)
# smo = Slider(max_out, 'MaxOut', 0, 2/dt, valinit=max_out_init)
skp = Slider(kp, 'Kp', 0, .1, valinit=kp_init)
ski = Slider(ki, 'Ki', 0, .2, valinit=ki_init)
skd = Slider(kd, 'Kd', 0, .03, valinit=kd_init)
smi = Slider(max_int, 'MaxInt', 0, 20, valinit=max_int_init)
smo = Slider(max_out, 'MaxOut', 0, 1, valinit=max_out_init)

def update(val):
    kp = skp.val
    ki = ski.val
    kd = skd.val
    max_int = smi.val
    min_int = -smi.val
    max_out = smo.val
    min_out = -smo.val
    pid = PID(kp, ki, kd, dt, max_int, min_int, max_out, min_out)
    pos = 0.
    s = []
    for frame in t:
        if frame == 0.:
            s.append(pos)
            continue
        pos += pid.compute(150, pos)
        s.append(pos)
    l.set_ydata(s)
    fig.canvas.draw_idle()

# Events
skp.on_changed(update)
ski.on_changed(update)
skd.on_changed(update)
smi.on_changed(update)
smo.on_changed(update)

plt.show()

