==========
MONOLOGUE
==========

This Python module offers an interface to unify:

- logging
    basically, standard Python logging with some boilerplate removed.
- progress information
    dots, loops count, completion percentages
    about an ongoing computation.


.. contents::

.. sectnum::


Licence
========

See COPYING: New BSD license (open to discussion).

Requirements and compatibility
==============================

.. TODO

Target to day is stock Python 2.5-7 with no requirement.

Python 2.7 works.

Here be moreinfo.

Concept
=========

This is meant to be 'easy' to use, even for non computer scientists and
required to work well even on very minimal exotic platforms such as Windows
console terminals.

The light from the most beautiful nebulae far up in the sky travels a long
time to reach us; likewise, it may be that a lot of computational time
separates you from the contemplation of an interesting result after you fed
a program heaps of data (for instance, modelisation with scikit-learn_).

It is good practice to impress the viewer with details about what's going on:
informative messages and/or progress information.
The purpose of this Python module is to help you do so.

.. _scikit-learn: http://scikit-learn.org

Differences with stock logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some things are deliberately different from logging.  This module will
be logging to stdout by default.

Loggers defined here here have a verbosity setting: this integer has the opposite
meaning of the "log level" from logging.

Progress information
~~~~~~~~~~~~~~~~~~~~~~~

All indicators below shown can be combined at will.

Running distance unknown
-------------------------------

If your program is looping in the dark, searching for a solution with the loop
number unknown, then maybe the best output you can do to say "hey, I'm alive,
I'm digging that mine out" is a plain old dot every given number of steps::

        .


Then, one minute later, another dot::

        ..


Many dots, and so on, you get it.

This can be combined with::

        ..........
        [Exciting computation] Iteration 1000 done
        ..........
        [Exciting computation] Iteration 2000 done
        ...


Running distance known
-------------------------------

It's fair, if you know your program is going to run through 42195 iterations a
particular loop, to let the viewer know how far it's gone::

        [Exciting computation] 10 %
        [Exciting computation] 20 %
        ...

This uses the plain logging system.

Logging and progress combined
---------------------------------

The combination of logging full lines and progress dots that are not
individually followed with a newline character involves a trick to end the line
before an informative message.


How to use
===========

Here be docs; for now there is a huge doctest that maybe ought to be split.

.. TODO


Roadmap
=======

- Handle CR/LF as well as ``\n``
    Read sys.platform, act accordingly.
- Handle other streams than sys.stdout
    If progress dots are to be printed on random streams,
    the handling of newlines may be a little tricky.
    A workaround is that the dev uses separate loggers (different names)
    if they intend to log to files and show progress.
- Lazy string formatting
    take advantage of this feature from logging (with a keyword)
- Color_?
    I doubt this works on Windows.
- Use configuration files?
    For some of the above features.

.. _Color:
   http://stackoverflow.com/questions/384076/how-can-i-make-the-python-logging-output-to-be-colored

From ideas to bytes
======================

Code monkey is Feth Arezki.

The idea behind this, and many ideas of how it should be done are Gael
Varoquaux's.  Also participated in the discussion, or motivated me: Olivier
Grisel, Fabian Pedregosa, Nelle Varoquaux. See
https://github.com/scikit-learn/scikit-learn/pull/130
