#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""A simple PID controller module.

LICENSE
=======
See __license__ below or read `pydoc pid`.

AUTHOR
======
See __author__ below or read `pydoc pid`.

HELP/USAGE
==========
See docstrings for usage of any particular submodule via either `pydoc pid`
    or interactively using `help(submodule)` or `pid.submodule?`.

REFERENCES
==========
1. wiki: https://en.wikipedia.org/wiki/PID_controller
2. PIDController: cgkit.sourceforge.net/doc2/pidcontroller.html#PIDController
3. pypid: https://pypi.python.org/pypi/pypid
4. Recipe: code.activestate.com/recipes/577231-discrete-pid-controller
5. O'Reilly: examples.oreilly.com/9780596809577/CH09/PID.py
6. Atmel example: http://www.atmel.com/images/doc2558.pdf
7. ECEE Paper: http://ecee.colorado.edu/shalom/Emulations.pdf

"""

__creator__ = 'Matt Busby'
__email__ = '<busby.gator@gmail.com>'
__date__ = ' '.join(['Created', '5/25/2015'])
__copyright__ = "Copyright (c) {year}, {owner}. All rights reserved.".format(\
        year=__date__.split('/')[-1], owner=__creator__)
__licence__ = """\
        BSD 3-Clause License

        {copyright}

        Redistribution and use in source and binary forms, with or without
        modification, are permitted provided that the following conditions
        are met:

        1. Redistributions of source code must retain the above copyright
           notice, this list of conditions and the following disclaimer.

        2. Redistributions in binary form must reproduce the above copyright
           notice, this list of conditions and the following disclaimer in
           the documentation and/or other materials provided with the
           distribution.

        3. Neither the name of the copyright holder nor the names of its
           contributors may be used to endorse or promote products derived
           from this software without specific prior written permission.

        THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
        "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
        LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
        FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
        COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
        INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
        BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
        LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
        CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
        LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY
        WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
        POSSIBILITY OF SUCH DAMAGE.
        """.format(copyright=__copyright__)
__author__ = '{0} {1}'.format(__creator__, __email__)
__credits__ = ', '.join((__creator__,)) + '.'
__versioninfo__ = (1, 0, 0)
__version__ = '.'.join(map(str, __versioninfo__))

from .pid import PID

__all__ = ['PID']

