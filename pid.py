#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""Discrete PID controller class.

For help, usage, copyright, license, creation, authors, references, and
    version data please see __init__.py, or read the metadata externally
    via either `pydoc pid` or interactively using `help(pid)` or `pid.PID?`.

"""
from __future__ import division, print_function

class PID(object):
    """Ideal PID controller class.

    USAGE
    =====
    In [1]: from pid import PID
    In [2]: pid = PID()

    TUNING (5.)
    ==========
    CL RESPONSE   RISE TIME      OVERSHOOT   SETTLING TIME   S-S ERROR
    -----------   ---------      ---------   -------------   ---------
    Kp            Decrease       Increase    Small Change    Decrease
    Ki            Decrease       Increase    Increase        Eliminate
    Kd            Small Change   Decrease    Decrease        No Change

    Ziegler-Nichols Parameters (6.)
    ==========
    Controller    Kp             Ti          Td
    -----------   ---------      ---------   ------------
    P             0.5*Kc
    PD            0.65*Kc                    0.12*Pc
    PI            0.45*Kc        0.85*Pc
    PID           0.65*Kc        0.5*Pc      0.12*Pc
    * With Use only P first until a systained and stable oscillation occurs,
      then use Pc: Oscillation period, Kc: Critical gain

    """
    def __init__(self, k_p=None,k_i=None, k_d=None, d_t=None, pid=None,
                 proportional=None, integral=None, derivative=None,
                 max_int=None, min_int=None, max_out=None, min_out=None):
        """Init class.

        Arguments
        =========
        k_p:          # Proportional constant
        k_i:          # Integral constant
        k_d:          # Derivative constant
        d_t:          # Delta time
        pid:          # PID type
        proportional: # Proportional method
        integral:     # Intrgration method
        derivative:   # Derivative method
        max_int:      # Limit integration term, eg to counteract intetral windup
        min_int:      # Limit integration term, eg to counteract intetral windup
        max_out:      # Clamp output value
        min_out:      # Clamp output value

        Help
        ====
        * Pick a time constant that is between 1/10th and 1/100th of the
          desired settling time.
        * If your time constant is very small, look into setting max/mins for
          your integrator.

        """
        self.k_p = k_p if k_p is not None else 1
        self.k_i = k_i if k_i is not None else 1/6
        self.k_d = k_d if k_d is not None else 0
        self.d_t = d_t if d_t is not None else 1/10
        self.pid = pid if pid in ('ideal', 'parallel', 'test') else 'parallel'
        self.proportional = proportional if proportional in ('error', \
                'measured') else 'error'
        self.integral = integral if integral in ('backward', \
                'forward', 'trapezoidal') else 'backward'
        self.derivative = derivative if derivative in ('error', \
                'measured') else 'error'
        self.max_int = max_int if max_int is not None else float('inf')
        self.min_int = min_int if min_int is not None else -float('inf')
        self.max_out = max_out if max_out is not None else float('inf')
        self.min_out = min_out if min_out is not None else -float('inf')
        self.int_ = 0.
        self.prev_meas = 0.
        self.prev_err = 0.
        self.prev_prev_err = 0.
        self.name = "{0:.2f}-{1:.2f}-{2:.3f}-{3:.2f}".format(self.k_p, \
                self.k_i, self.k_d, self.d_t)

    def __del__(self):
        pass

    def __str__(self):
        str_ = '<{0} {1}:'.format(self.__class__.__name__, self.name)
        for each in dir(self):
            if each and each[0] != '_' and each != 'name':
                attr = getattr(self, each)
                if not callable(attr):
                    str_ += ' {0}={1}'.format(each, attr)
        str_ += '>'
        return str_

    def reset(self):
        """Set new internal position."""
        self.int_ = 0.
        self.prev_meas = 0.
        self.prev_err = 0.
        self.prev_prev_err = 0.

    def compute(self, set_, meas):
        """Compute state of PID based on setpoint and measured value.

        set_: Setpoint (target)
        meas: Actual measured value

        """
        # Error
        err = set_ - meas

        # P
        if self.proportional == 'error':
            pro = err
        elif self.proportional == 'measured':
            pro = -meas

        # I
        if self.integral == 'backward':
            self.int_ += (err * self.d_t)
        elif self.integral == 'forward':
            self.int_ += (self.prev_err * self.d_t)
        elif self.integral == 'trapezoidal':
            self.int_ += (((err + self.prev_err) / 2.) * self.d_t)
        if self.int_ > self.max_int:
            self.int_ = self.max_int
        elif self.int_ < self.min_int:
            self.int_ = self.min_int

        # D
        if self.derivative == 'error':
            der = (err - self.prev_err) / self.d_t
        elif self.derivative == 'measured':
            der = -(meas - self.prev_meas) / self.d_t

        # Sum
        if self.pid == 'parallel':
            err_out = pro*self.k_p + self.int_*self.k_i + der*self.k_d
        elif self.pid == 'ideal':
            err_out = self.k_p * (pro + self.int_*self.k_i + der*self.k_d)
        elif self.pid == 'test':
            k_1 = self.k_p + self.k_i + self.k_d
            k_2 = -self.k_p - 2 * self.k_d
            k_3 = self.k_d
            err_out = k_1 * err + k_2 * self.prev_err * self.d_t + k_3 * self.prev_prev_err / self.d_t

        # Clamp output
        if err_out > self.max_out:
            err_out = self.max_out
        if err_out < self.min_out:
            err_out = self.min_out

        self.prev_meas = meas
        self.prev_prev_err = self.prev_err
        self.prev_err = err

        return err_out

