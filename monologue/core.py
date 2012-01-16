"""
Utility module to log and indicate the progress of any job that use loops.

=================
New BSD License
=================

Copyright (c) 2011-2012 Feth Arezki.
All rights reserved.


Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

  a. Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.
  b. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.
  c. Neither the name of the Scikit-learn Developers  nor the names of
     its contributors may be used to endorse or promote products
     derived from this software without specific prior written
     permission.


THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE REGENTS OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH
DAMAGE.

=================================
TL; DR (too long, did'nt read)
=================================

>>> logger = get_logger("identifier")
>>> logger.msg("blah")
[identifier] blah
>>> logger.set_dot_char("x")  # doctest prefers x to .
>>> for time in xrange(5): logger.dot()
xxxxx

===================================
Doc
===================================
For now, a doctest in monologue/tests/

"""


from __future__ import division
import sys
from logging import DEBUG, CRITICAL, Formatter, INFO, Logger, StreamHandler
from functools import wraps


DOT = 0
TEXT = 1
PROGRESS = INFO - 5  # == DEBUG + 5
REFERENCE_LEVEL = PROGRESS
DEFAULT_DOT_CHAR = "."

# global variable (baah) for output type
LAST_OUT = TEXT

# used by getLogger
_LOGGERS = {}

# In order to never print a percent indicator, the finite value for 'never'
_NEVER_PERCENT_VALUE = 0


def _set_out_type(new):
    """
    As we  don't want to mix progress dots and text on the same line,
    we insert a linebreak whenever the output type changes.

    Parameters
    ----------
    new: DOT or TEXT
    """
    global LAST_OUT

    if LAST_OUT is None:
        # initialize and return
        LAST_OUT = new
        return
    elif new == LAST_OUT:
        #no change
        return
    elif new == TEXT:
        sys.stdout.write('\n')
    LAST_OUT = new


def _textlogger_factory(klass, attr_name):
    """
    Adds a call to _set_out_type to the vanilla function
    taken in klass.

    This factory is used at class initialization time to wrap
    Logger.debug() and family in ProgressAndLog,
    in order to insert newlines between dots and log messages.
    """
    func = getattr(klass, attr_name)

    @wraps(func)
    def new_func(*args, **kwargs):
        _set_out_type(TEXT)
        func(*args, **kwargs)
    return new_func


class ProgressAndLog(Logger):
    """
    Subclass of Logger, this class combines 2 functionnalities:
    -print messages
    -report computing progress

    Logger API: http://docs.python.org/library/logging.html#logger-objects

    """
    def __init__(self, name, verbosity_offset):
        Logger.__init__(self, name)

        # overwritten by set_offset
        # this is an emulation of the Logger level for dots
        self._offset = verbosity_offset
        self._iterations = 0
        self._progress_every = 0
        self._dot_every = 1
        self._percent_print_every = 0
        self._next_percent_print = _NEVER_PERCENT_VALUE
        self._percent_target = _NEVER_PERCENT_VALUE

        formatter = Formatter(fmt="[%(name)s] %(message)s")

        handler = StreamHandler(sys.stdout)
        handler.setFormatter(formatter)

        self.addHandler(handler)

        self.set_offset(verbosity_offset)

        self._dot_char = DEFAULT_DOT_CHAR

    debug, info, warning, critical = (_textlogger_factory(Logger, name)
        for name in 'debug info warning critical'.split())

    def msg(self, message, verbosity=None):
        """
        Prints out an msg.
        Conditionnal to verbosity settings

        Parameters
        ----------
        message: text string

        verbosity: optional; boolean or integer.
            if False, the message is only displayed when the logger
        """
        if verbosity in (True, None):
            verbosity = CRITICAL
        elif verbosity is False:
            verbosity = DEBUG
        _set_out_type(TEXT)
        Logger.log(self, verbosity, message)

    def dot(self, verbosity=None):
        """
        Spits out a dot.
        Conditionnal to verbosity settings

        Parameters
        ----------
        verbosity: see ProgressAndLog.msg
        """
        output = False
        if verbosity in (True, None):
            # True: explicitely asked to spit the dot.
            # None, default value: always spit a dot.
            output = True
        elif verbosity is False:
            # Only spitting the dot if we're a very verbose logger
            output = self._offset < 0
        else:
            # Not None or a bool? expecting an int
            output = self._offset <= REFERENCE_LEVEL - verbosity
        if output:
            _set_out_type(DOT)
            sys.stdout.write(self._dot_char)

    def set_offset(self, offset):
        self._offset = offset
        self.setLevel(offset + REFERENCE_LEVEL)

    def add_to_offset(self, value):
        self.set_offset(self._offset + value)

    def setLevel(self, level):
        self._offset = level - REFERENCE_LEVEL
        Logger.setLevel(self, level)

    def progress_every(self, value):
        """
        Configures ProgressAndLog to spit out a progress indication
        once every for every <value> times progress_step() is called
        """
        self._progress_every = value

    def dot_every(self, value):
        """
        value: int
        Configures ProgressAndLog to spit out a dot once every for every
        <value> times progress_step() is called or never if <value> is < 1
        """
        self._dot_every = value

    def set_dot_char(self, char):
        self._dot_char = char

    def progress_reset(self):
        self._iterations = 0
        self._next_percent_print = self.percent_print_every

    def offset(self):
        return self._offset

    def _maybe_dot(self):
        if self._dot_every > 0 \
            and self.getEffectiveLevel() <= PROGRESS \
            and not self._iterations % self._dot_every:
            self.dot()

    def _maybe_iteration_msg(self):
        if self._progress_every < 1:
            return
        if not self._iterations % self._progress_every:
            message = "Iteration %d done" % self._iterations
            self.msg(message, verbosity=PROGRESS)

    def _maybe_percentage_msg(self):
        if self._percent_target <= 0:
            return

        current_percentage = 100 * (self._iterations / self._percent_target)
        if current_percentage < self._next_percent_print:
            return

        self.msg("%d%%" % self._next_percent_print)
        self._next_percent_print += self._percent_print_every

    def progress_step(self):
        """
        Call this every time you perform a loop.
        If a message or a dot needs to be spit every 1000 iterations,
        this function will take care.
        """
        self._iterations += 1

        # keep dot first, it's prettier.
        self._maybe_dot()
        self._maybe_iteration_msg()
        self._maybe_percentage_msg()

    def percent_target(self, value):
        self._percent_target = value

    def progress_complete(self, verbosity=None):
        """
        Call this upon completion to print out a message with the number
        of performed iterations.
        Iterations counting will be reset

        verbosity has the same meaning as in ProgressAndLog.dot
        and ProgressAndLog.msg
        """
        self.msg("Successfully completed %d iterations" % self._iterations)
        self._iterations = 0
        self._next_percent_print = _NEVER_PERCENT_VALUE
        self._percent_target = _NEVER_PERCENT_VALUE

    def percent_print_every(self, value):
        """
        We'll print some progress information every that percent
        """
        self._percent_print_every = value


def get_logger(name, verbosity_offset=0):
    """
    Provides a logger with specified name.
    """
    logger = _LOGGERS.get(name)
    if logger is None:
        logger = ProgressAndLog(name, verbosity_offset=verbosity_offset)
        _LOGGERS[name] = logger
        # verbosity_offset is ignored after the 1st call
    return logger


def reset_newline():
    """
    Ensure you don't get a spurious \n when logging
    in weird conditions after re-importing this module
    """
    global LAST_OUT
    LAST_OUT = TEXT
