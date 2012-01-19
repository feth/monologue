#coding: utf-8
"""
tests for logger.py prior to coding

I'll fix docstring formatting, I promise.
I'll split this as soon as I fugure out how to do it.

We are testing the global Logger level, but this does not harm the
possibility of adding a log handler to a logger, with a specific log level.
However, most progress_* functions do bypass the traditional logging mechanism.

Test internals
==============
>>> from .. import core
>>> core.reset_newline()
>>> core.LAST_OUT == core.TEXT  # must be True on first import or after reset_newline
True

Creation of loggers
===================
>>> from .. import get_logger, PROGRESS
... # PROGRESS is a custom level (DEBUG + 5)
>>> from logging import DEBUG, INFO, WARNING
>>> verbose_logger = get_logger("ver",
... verbosity_offset=-10)
>>> verbose_logger.getEffectiveLevel()
5
>>> standard_logger = get_logger("std")
>>> PROGRESS
15
>>> standard_logger.getEffectiveLevel()
15
>>> laconic_logger = get_logger("lac",
... verbosity_offset=+10)

Play with verbosity (absolute)
------------------------------
>>> laconic_logger.setLevel(DEBUG)
>>> laconic_logger.debug("Message must be displayed")
[lac] Message must be displayed
>>> laconic_logger.setLevel(PROGRESS)
>>> laconic_logger.setLevel(WARNING)


progress
========

Initialization
>>> for logger in (verbose_logger, standard_logger, laconic_logger):
...    logger.progress_every(1000)
>>> for logger in (verbose_logger, standard_logger, laconic_logger):
...    logger.dot_every(10)

progress_step
-------------
>>> progress_logger = get_logger("progress")
>>> progress_logger.setLevel(PROGRESS)
>>> progress_logger.set_dot_char('x')

Testing dots alone
~~~~~~~~~~~~~~~~~~
>>> for count in range(10):
...     progress_logger.progress_step()
xxxxxxxxxx

>>> progress_logger.progress_reset()
>>> progress_logger.dot_every(10)

>>> for count in range(9):
...     progress_logger.progress_step()
>>> progress_logger.progress_step()
x

>>> for count in range(90):
...     progress_logger.progress_step()
xxxxxxxxx

>>> progress_logger.info('eat newline after xxxxxxxx')
<BLANKLINE>
[progress] eat newline after xxxxxxxx

Testing progress alone
~~~~~~~~~~~~~~~~~~~~~~~
>>> progress_logger.dot_every(0)
>>> for count in range(90):
...     progress_logger.progress_step()

>>> progress_logger.progress_reset()
>>> progress_logger.progress_every(1)
>>> for count in range(3):
...     progress_logger.progress_step()
[progress] Iteration 1 done
[progress] Iteration 2 done
[progress] Iteration 3 done

>>> progress_logger.progress_reset()
>>> progress_logger.progress_every(1000)
>>> for count in range(2000):
...     progress_logger.progress_step()
[progress] Iteration 1000 done
[progress] Iteration 2000 done

Testing progress AND dots
~~~~~~~~~~~~~~~~~~~~~~~~~
>>> progress_logger.progress_reset()
>>> progress_logger.dot_every(1)
>>> progress_logger.progress_every(1)
>>> progress_logger.progress_step()
x
[progress] Iteration 1 done

>>> progress_logger.progress_reset()
>>> for count in range(4):
...     progress_logger.progress_step()
x
[progress] Iteration 1 done
x
[progress] Iteration 2 done
x
[progress] Iteration 3 done
x
[progress] Iteration 4 done

>>> progress_logger.progress_reset()
>>> progress_logger.set_offset(+0)
>>> progress_logger.dot_every(100)
>>> progress_logger.progress_every(1000)
>>> for count in range(2000):
...     progress_logger.progress_step()
xxxxxxxxxx
[progress] Iteration 1000 done
xxxxxxxxxx
[progress] Iteration 2000 done

#Same, with a higher print offset
>>> progress_logger.progress_reset()
>>> progress_logger.set_offset(+10)
>>> for count in range(2000):
...     progress_logger.progress_step()
>>> progress_logger.progress_complete()
[progress] Successfully completed 2000 iterations
>>> standard_logger.percent_print_every(10)
... # every 10 percent, requires a target
>>> standard_logger.percent_target(1000) # the scale. rename function?
>>> standard_logger.dot_every(0)
>>> standard_logger.progress_every(0)
>>> for count in range(2000):
...     standard_logger.progress_step()
[std] 0%
[std] 10%
[std] 20%
[std] 30%
[std] 40%
[std] 50%
[std] 60%
[std] 70%
[std] 80%
[std] 90%
[std] 100%
[std] 110%
[std] 120%
[std] 130%
[std] 140%
[std] 150%
[std] 160%
[std] 170%
[std] 180%
[std] 190%
[std] 200%


"""
