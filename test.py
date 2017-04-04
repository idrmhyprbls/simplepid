#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Test PID controllers using nose.

USAGE
=====
$ nosetests pid
- or -
$ python -m pid.test_pid

For further help, usage, copyright, license, creation, authors, references, and
    version data please see __init__.py, or read the metadata externally
    via either `pydoc pid` or interactively using `help(pid)` or `pid.PID?`.

"""
from __future__ import division, print_function

from .pid import PID

try:
    import matplotlib.pyplot as plt
except ImportError:
    raise ImportError("No module: matplotlib! Please install for your env.")
try:
    import numpy
except ImportError:
    raise ImportError("No module: numpy! Please install for your env.")

class TestPID(object):
    """Nose test class using discrete time."""
    d_t = 1/30.
    smax = 20
    ymax = 220
    p0 = 30
    sp = 180

    def __init__(self):
        pass

    @classmethod
    def setup_class(cls):
        """Sets up the test."""
        pass

    @classmethod
    def teardown_class(cls):
        """Tears down the test."""
        plt.legend()
        plt.show()

    def test_compass(self):
        """Test PID group."""
        self.d_t = 1/30.
        self.smax = 20
        self.ymax = 220
        self.p0 = 30
        self.sp = 180

        plt.axis([0, self.smax, self.p0, self.ymax])
        x = numpy.arange(0., self.smax, self.d_t)
        y = numpy.ones(len(x)) * self.sp
        plt.plot(x, y)

        # Best tuning
        pid = PID(.09, .25, .02, self.d_t, 'parallel', \
                  'error', 'trapezoidal', 'error', \
                  8, -8, 12 * self.d_t, -12 * self.d_t)
        self.impulse(pid)

        # Using dt?
        pid = PID(1.5 * self.d_t, self.d_t * 2, 0, self.d_t, 'parallel', \
                  'error', 'trapezoidal', 'error')
        self.impulse(pid)

        # Test
        pid = PID(.1, 0.3, 0.05, self.d_t, 'ideal', \
                  'error', 'trapezoidal', 'measured')
        self.impulse(pid)

    def impulse(self, pid):
        """Plot PID with impulse response."""
        xaxis = numpy.arange(0., self.smax, pid.d_t)
        yaxis = []
        pid.reset()
        pos = self.p0
        for time in xaxis:
            if time == 0.:
                yaxis.append(pos)
                continue
            err = pid.compute(self.sp, pos)
            pos += err
            yaxis.append(pos)
        plt.plot(xaxis, yaxis, '-', label=pid.name)

    def plot_pid(self, pid):
        """Plot PID with impulse response."""
        xaxis = numpy.arange(0., self.smax, pid.d_t)
        track = ([100]*180 + \
                 [80]*180 + \
                 [150]*1000 \
                 )[:len(xaxis)]
        yaxis = []
        pid.reset()
        pos = 50.
        for frame,time in enumerate(xaxis):
            if time == 0.:
                yaxis.append(pos)
                continue
            err = pid.compute(track[frame], pos)
            pos += err
            yaxis.append(pos)
        plt.plot(xaxis, yaxis, '-', label=pid.name)
        plt.plot(xaxis, track[frame], '-')

if __name__ == '__main__':
    import sys
    mytest = TestPID()
    mytest.setup_class()
    mytest.test_compass()
    mytest.teardown_class()
    del mytest
    sys.exit()
    try:
        import nose
    except ImportError:
        raise ImportError("No module: nose! Please install for your env.")
    sys.exit(nose.run())

