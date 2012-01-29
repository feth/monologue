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
  c. Neither the name of the Monologue Developers nor the names of
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
>>> logger.set_dot_string("x")  # doctest prefers x to .
>>> for time in xrange(5): logger.dot()
xxxxx

===================================
Doc
===================================
Sphinx doc is almost complete, as well as docstrings here.

"""


from __future__ import division
import sys
import os
from logging import DEBUG, CRITICAL, Formatter, INFO, Logger, StreamHandler
from functools import wraps
from weakref import WeakKeyDictionary


DOT = 0
TEXT = 1
PROGRESS = INFO - 5  # == DEBUG + 5
REFERENCE_LEVEL = PROGRESS
DEFAULT_DOT_CHAR = "."

# used by getLogger
_LOGGERS = {}
#used by _set_out_type
_OUT_TYPES = WeakKeyDictionary()

# In order to never print a percent indicator, the finite value for 'never'
_NEVER_PERCENT_VALUE = 0


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
    def new_func(self, *args, **kwargs):
        self._set_out_type(TEXT)
        return func(self, *args, **kwargs)

    return new_func


class ProgressAndLog(Logger):
    """
    Subclass of Logger, this class combines 2 functionnalities:
    -print messages
    -report computing progress

    Logger API: http://docs.python.org/library/logging.html#logger-objects

    traditional logging functions still work
    ========================================
    #boilerplate initialization
    >>> from logging import DEBUG, INFO, WARNING
    >>> verbose_logger = get_logger("test.logging.ver", verbosity_offset=-10)
    >>> standard_logger = get_logger("test.logging.std")
    >>> laconic_logger = get_logger("test.logging.lac", verbosity_offset=+10)
    >>> verbose_logger.debug("Message must be displayed")
    [test.logging.ver] Message must be displayed
    >>> standard_logger.debug("Message mustn't be displayed")
    >>> laconic_logger.debug("Message mustn't be displayed")

    >>> verbose_logger.info("Message must be displayed")
    [test.logging.ver] Message must be displayed
    >>> standard_logger.info("Message must be displayed")
    [test.logging.std] Message must be displayed
    >>> laconic_logger.info("Message mustn't be displayed")

    >>> verbose_logger.warning("Message must be displayed")
    [test.logging.ver] Message must be displayed
    >>> standard_logger.warning("Message must be displayed")
    [test.logging.std] Message must be displayed
    >>> laconic_logger.warning("Message must be displayed")
    [test.logging.lac] Message must be displayed

    corner cases
    ============

    mixing of progress messages and dots
    ------------------------------------
    >>> logger = get_logger("test.mix_progress_dots")
    >>> logger.progress_every(1)
    >>> logger.set_dot_string('x')
    >>> logger.progress_step()
    x
    [test.mix_progress_dots] Iteration 1 done

    >>> logger.progress_reset()
    >>> for count in range(4):
    ...     logger.progress_step()
    x
    [test.mix_progress_dots] Iteration 1 done
    x
    [test.mix_progress_dots] Iteration 2 done
    x
    [test.mix_progress_dots] Iteration 3 done
    x
    [test.mix_progress_dots] Iteration 4 done

    >>> logger.progress_reset()
    >>> logger.set_offset(+0)
    >>> logger.dot_every(100)
    >>> logger.progress_every(1000)
    >>> for count in range(2000):
    ...     logger.progress_step()
    xxxxxxxxxx
    [test.mix_progress_dots] Iteration 1000 done
    xxxxxxxxxx
    [test.mix_progress_dots] Iteration 2000 done
    """
    def __init__(self, name, verbosity_offset, logfile=None, timestamp=False):
        """
        Parameters
        ----------

        name: string
            is likely to end up between
            brackets at the beggining of each message
        verbosity_offset: integer
            see add_to_offset and the like
        logfile: see ProgressAndLog.add_logfile
        timestamp:  boolean, defaults to False
            defines:
            - whether the first logfile (or stdout) will contain timestamps
            - default value for future calls to add_logfile

        """
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
        self._logfiles = []
        self._dot_logfiles = []
        self._timestamp = timestamp
        self.add_logfile(logfile, timestamp=timestamp)

        self.set_offset(verbosity_offset)

        self._dot_string = DEFAULT_DOT_CHAR

    debug, info, warning, critical, log = (_textlogger_factory(Logger, name)
        for name in 'debug info warning critical log'.split())

    def add_logfile(self, logfile, dots=True, timestamp=None):
        """
        Parameters
        ----------

        logfile: string or open file, optional, default: sys.stdout
            we'll log messages and progress there.
            if a string is supplied, it is assumed to be the path where to log
            The file will be created or appended to.

        dots: boolean
            do you want dots printed in this logfile?

        timestamp: boolean, defaults to None
            do you want logs to be prefixed by a timestamp?
            if unset (None), the value set at object
            initialization (in __init__) is reused
        """
        if logfile is None:
            logfile = sys.stdout
        elif isinstance(logfile, basestring):
            logfile = open(logfile, 'ab')


        if timestamp is None:
            timestamp = self._timestamp
        if timestamp:
            log_format = "[%(asctime)s][%(name)s] %(message)s"
        else:
            log_format = "[%(name)s] %(message)s"
        formatter = Formatter(fmt=log_format)

        handler = StreamHandler(logfile)
        handler.setFormatter(formatter)
        self.addHandler(handler)

        self._logfiles.append(logfile)
        if dots:
            self._dot_logfiles.append(logfile)

    def msg(self, message, verbosity=None, msgvars=()):
        """
        Prints out an msg.
        Conditionnal to verbosity settings

        Parameters
        ----------
        message: text string
        verbosity: optional; boolean or integer.
            if False, the message is only displayed when the logger
            is as verbose as DEBUG or more
        msgvars: tuple or anything: mapping (dict), string, lists...
            as suitable for text suitable for substitution.
            message will be logged as ``message % msgvars``
            tuple is handled specifically, all the rest is used in
            a single placeholder


        msgvars allows for late evaluation of string formatting, therefore
        the formatting is not performed if the message should not be displayed
        at all

        Always print if verbosity not specified
        -------------------------------------

        #boilerplate initialization
        >>> from logging import DEBUG, INFO, WARNING
        >>> verbose_logger = get_logger("test.msg.ver", verbosity_offset=-10)
        >>> standard_logger = get_logger("test.msg.std")
        >>> laconic_logger = get_logger("test.msg.lac", verbosity_offset=+10)
        >>> verbose_logger.msg("Message must be displayed")
        [test.msg.ver] Message must be displayed
        >>> standard_logger.msg("Message must be displayed")
        [test.msg.std] Message must be displayed
        >>> laconic_logger.msg("Message must be displayed")
        [test.msg.lac] Message must be displayed

        Print according to verbosity
        -------------------------------------
        - verbosity=False => DEBUG
        - verbosity=True => always print
        - verbosity=int => use int as verb level
        Maybe this makes the case of ``verbosity in (0, 1)`` counter intuitive?

        False
        >>> verbose_logger.msg("Message must be displayed", verbosity=False)
        [test.msg.ver] Message must be displayed
        >>> standard_logger.msg("Message must'nt be displayed",
        ... verbosity=False)
        >>> laconic_logger.msg("Message must'nt be displayed", verbosity=False)

        True
        >>> verbose_logger.msg("Message must be displayed", verbosity=True)
        [test.msg.ver] Message must be displayed
        >>> standard_logger.msg("Message must be displayed", verbosity=True)
        [test.msg.std] Message must be displayed
        >>> laconic_logger.msg("Message must be displayed", verbosity=True)
        [test.msg.lac] Message must be displayed

        0 (same for 1)
        >>> verbose_logger.msg("Message mustn' be displayed", verbosity=0)
        >>> standard_logger.msg("Message must'nt be displayed", verbosity=0)
        >>> laconic_logger.msg("Message must'nt be displayed", verbosity=0)

        DEBUG (10)
        >>> verbose_logger.msg("Message must be displayed", verbosity=DEBUG)
        [test.msg.ver] Message must be displayed
        >>> standard_logger.msg("Message must'nt be displayed",
        ... verbosity=DEBUG)
        >>> laconic_logger.msg("Message must'nt be displayed", verbosity=DEBUG)

        INFO (20)
        >>> verbose_logger.msg("Message must be displayed", verbosity=INFO)
        [test.msg.ver] Message must be displayed
        >>> standard_logger.msg("Message must be displayed", verbosity=INFO)
        [test.msg.std] Message must be displayed
        >>> laconic_logger.msg("Message must'nt be displayed", verbosity=INFO)

        WARN (30)
        >>> verbose_logger.msg("Message must be displayed", verbosity=WARNING)
        [test.msg.ver] Message must be displayed
        >>> standard_logger.msg("Message must be displayed", verbosity=WARNING)
        [test.msg.std] Message must be displayed
        >>> laconic_logger.msg("Message must be displayed", verbosity=WARNING)
        [test.msg.lac] Message must be displayed

        Play with verbosity offset
        --------------------------
        For absolute verbosity, use setLevel (see below).
        >>> laconic_logger.msg("Message must'nt be displayed", verbosity=False)
        >>> laconic_logger.set_offset(-10) # relative to general level
        ... # which is INFO
        >>> laconic_logger.msg("Message must be displayed", verbosity=False)
        [test.msg.lac] Message must be displayed
        >>> laconic_logger.add_to_offset(20)
        ... #add_to_offset will get us back to the initial +10 value
        >>> laconic_logger.msg("Message must'nt be displayed", verbosity=False)

        Add some formatting
        --------------------
        >>> logger = get_logger("test.msg_placeholder")
        >>> logger.msg("Message with 1 placeholder [[%s]]",
        ... msgvars="placed_data")
        [test.msg_placeholder] Message with 1 placeholder [[placed_data]]
        >>> logger.msg("Message with 2 placeholders [[%s]] [[%s]]",
        ... msgvars=("data 1", "data 2")) #doctest: +NORMALIZE_WHITESPACE
        [test.msg_placeholder] Message with 2 placeholders [[data 1]]
        [[data 2]]
        >>> logger.msg("Message with dict formatting [[%(value 1)s, "
        ... "%(value 2)s]]", msgvars={"value 1": "aaa", "value 2": "bbb"},)
        [test.msg_placeholder] Message with dict formatting [[aaa, bbb]]

        """
        if verbosity in (True, None):
            verbosity = CRITICAL
        elif verbosity is False:
            verbosity = DEBUG
        self._set_out_type(TEXT)
        if isinstance(msgvars, tuple):
            # Logger.log wants tuples to be given as *args
            Logger.log(self, verbosity, message, *msgvars)
        else:
            Logger.log(self, verbosity, message, msgvars)

    def dot(self, verbosity=None, dot_string=None):
        """
        Spits out a dot.
        Conditionnal to verbosity settings

        Parameters
        ----------
        verbosity: optional, see ProgressAndLog.msg
        dot_string: optional, string
            this string, likely "." or "x"... will be used this time only
            This allows to tell information about the computation going on.
            Examples::

                [5][3][2][3][2][8][2][3]
                or
                ....X........X...............

        #boilerplate initialization
        >>> from logging import DEBUG, INFO, WARNING
        >>> verbose_logger = get_logger("ver", verbosity_offset=-10)
        >>> standard_logger = get_logger("std")
        >>> laconic_logger = get_logger("lac", verbosity_offset=+10)

        dot overriding
        >>> for time in xrange(2):
        ...     verbose_logger.dot(dot_string="[more than a dot]")
        [more than a dot][more than a dot]

        no verbosity: always output
        >>> verbose_logger.dot() # doctest: +NORMALIZE_WHITESPACE
        .
        >>> standard_logger.dot() # doctest: +NORMALIZE_WHITESPACE
        .
        >>> laconic_logger.dot() # doctest: +NORMALIZE_WHITESPACE
        .

        verbosity=False -> DEBUG
        >>> verbose_logger.dot(verbosity=False)
        .
        >>> standard_logger.dot(verbosity=False)
        >>> laconic_logger.dot(verbosity=False)

        verbosity=True -> always print
        >>> verbose_logger.dot(verbosity=True)
        .
        >>> standard_logger.dot(verbosity=True)
        .
        >>> laconic_logger.dot(verbosity=True)
        .

        verbosity=PROGRESS for instance
        >>> verbose_logger.dot(verbosity=PROGRESS)
        .
        >>> standard_logger.dot(verbosity=PROGRESS)
        .
        >>> laconic_logger.dot(verbosity=PROGRESS)

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
            if dot_string is None:
                dot_string = self._dot_string
            self._set_out_type(DOT)
            for logfile in self._dot_logfiles:
                logfile.write(dot_string)

    def set_offset(self, offset):
        """
        Sets verbosity offset above/below standard verbosity level.

        Parameters:
        offset: integer
            makes sense between -5 and +35

        >>> logger = get_logger("test.offset")
        >>> logger.set_offset(+10)
        >>> logger.offset()
        10
        >>> logger.getEffectiveLevel()
        25
        """
        self._offset = offset
        self.setLevel(offset + REFERENCE_LEVEL)

    def add_to_offset(self, value):
        """

        """
        self.set_offset(self._offset + value)

    def setLevel(self, level):
        self._offset = level - REFERENCE_LEVEL
        Logger.setLevel(self, level)

    setLevel.__doc__ = Logger.setLevel.__doc__

    def progress_every(self, value):
        """
        parameters
        ----------
        value: int
            Configures ProgressAndLog.progress_step() to spit out
            an informative line
            - if <value> is < 1: never
            - else: once every for every <value> times

        #boilerplate initialization
        >>> logger = get_logger("test.progress_every")
        >>> logger.setLevel(PROGRESS)
        >>> logger.progress_reset()


        #testing progress alone: prevent dots
        >>> logger.dot_every(0)


        >>> logger.progress_every(1)
        >>> for count in range(3):
        ...     logger.progress_step()
        [test.progress_every] Iteration 1 done
        [test.progress_every] Iteration 2 done
        [test.progress_every] Iteration 3 done

        >>> logger.progress_reset()
        >>> logger.progress_every(1000)
        >>> for count in range(2000):
        ...     logger.progress_step()
        [test.progress_every] Iteration 1000 done
        [test.progress_every] Iteration 2000 done
        """
        self._progress_every = value

    def dot_every(self, value):
        """
        parameters
        ----------
        value: int
            Configures ProgressAndLog.progress_step() to spit out a dot
            - if <value> is < 1: never
            - else: once every for every <value> times

        #boilerplate initialization
        >>> logger = get_logger("test.dot_every")
        >>> logger.setLevel(PROGRESS)
        >>> logger.set_dot_string('x')

        #ensure indicators are blank
        >>> logger.progress_reset()

        >>> logger.dot_every(10)
        >>> for count in range(9):
        ...     logger.progress_step()
        >>> logger.progress_step()
        x
        >>> for count in range(90):
        ...     logger.progress_step()
        xxxxxxxxx
        """
        self._dot_every = value

    def set_dot_string(self, dot_string):
        """
        Set the string to be used to mark progression

        Parameters
        ----------
        dot_string: optional, string
            this string, likely "." or "x"... will be used this time only
        """
        self._dot_string = dot_string

    def progress_reset(self):
        """
        Call this to reset the number of iterations performed.
        Subsequent iterations will be numbered 1, 2 etc
        """
        self._iterations = 0
        self._next_percent_print = self.percent_print_every

    def offset(self):
        """
        Getter for the current verbosity offset
        """
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

        #boilerplate initialization
        >>> logger = get_logger("test.progress_step")
        >>> logger.setLevel(PROGRESS)
        >>> logger.set_dot_string('x')

        Testing dots alone
        ~~~~~~~~~~~~~~~~~~
        >>> for count in range(10):
        ...     logger.progress_step()
        xxxxxxxxxx

        #Keep next to previous test (dots alone)
        >>> logger.info('eat newline after xxxxxxxx')
        <BLANKLINE>
        [test.progress_step] eat newline after xxxxxxxx

        Testing progress alone
        ~~~~~~~~~~~~~~~~~~~~~~~
        >>> logger.dot_every(0)
        >>> for count in range(90):
        ...     logger.progress_step()

        """
        self._iterations += 1

        # keep dot first, it's prettier.
        self._maybe_dot()
        self._maybe_iteration_msg()
        self._maybe_percentage_msg()

    def percent_target(self, value):
        """
        Call this to set the number of expected iterations
        Also call percent_print_every()
        >>> logger = get_logger("test.percent")
        >>> logger.percent_print_every(10)
        ... # every 10 percent, requires a target
        >>> logger.percent_target(1000) # the scale. rename function?
        >>> logger.dot_every(0)
        >>> logger.progress_every(0)
        >>> for count in range(2000):
        ...     logger.progress_step()
        [test.percent] 0%
        [test.percent] 10%
        [test.percent] 20%
        [test.percent] 30%
        [test.percent] 40%
        [test.percent] 50%
        [test.percent] 60%
        [test.percent] 70%
        [test.percent] 80%
        [test.percent] 90%
        [test.percent] 100%
        [test.percent] 110%
        [test.percent] 120%
        [test.percent] 130%
        [test.percent] 140%
        [test.percent] 150%
        [test.percent] 160%
        [test.percent] 170%
        [test.percent] 180%
        [test.percent] 190%
        [test.percent] 200%
        """
        self._percent_target = value

    def progress_complete(self, verbosity=None):
        """
        Call this upon completion to print out a message with the number
        of performed iterations.
        Iterations counting will be reset

        verbosity has the same meaning as in ProgressAndLog.dot
        and ProgressAndLog.msg
        >>> logger = get_logger("test.progress_complete")

        # inhibit dots
        >>> logger.set_offset(+10)
        >>> for count in range(2000):
        ...     logger.progress_step()
        >>> logger.progress_complete()
        [test.progress_complete] Successfully completed 2000 iterations
        """
        self.msg("Successfully completed %d iterations" % self._iterations,
                verbosity=verbosity)
        self._iterations = 0
        self._next_percent_print = _NEVER_PERCENT_VALUE
        self._percent_target = _NEVER_PERCENT_VALUE

    def percent_print_every(self, value):
        """
        We'll print some progress information every that percent
        """
        self._percent_print_every = value

    def _set_out_type(self, new):
        """
        As we  don't want to mix progress dots and text on the same line,
        we insert a linebreak whenever the output type changes.

        Parameters
        ----------
        new: DOT or TEXT
        """
        for logfile in self._dot_logfiles:
            if logfile not in _OUT_TYPES:
                _OUT_TYPES[logfile] = TEXT
                last_out = TEXT
            else:
                last_out = _OUT_TYPES[logfile]

            if new == last_out:
                continue
            elif new == TEXT:
                logfile.write(os.linesep)

            _OUT_TYPES[logfile] = new


def get_logger(name, verbosity_offset=0, logfile=None, timestamp=False):
    """
    Provides a logger with specified name.
    """
    logger = _LOGGERS.get(name)
    if logger is None:
        logger = ProgressAndLog(name, verbosity_offset=verbosity_offset,
                logfile=logfile, timestamp=timestamp)
        _LOGGERS[name] = logger
        # verbosity_offset is ignored after the 1st call with a given name.
        # should we change it instead?
        # Principle of least astonishment drives me towards wanting
        # the removal of the keyword ``verbosity_offset`` in get_logger().
        # Also, what to to when a logger is configured with a given logfile and
        # the second call asks for another? yell to stderr?
        # Comments welcome.
    return logger
