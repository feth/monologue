==========
MONOLOGUE
==========

This Python module offers an interface to unify:

- logging
    basically, standard Python logging with some boilerplate removed.
- progress information
    dots, loops count, completion percentages
    about an ongoing computation.


WARNING
#########

It seems github is not rendering this rst file correctly. Until I fix this, I advise you to run ``make pdf``
in the source directory.


.. contents::

.. sectnum::


License
#########

.. compound::

    .. include:: COPYING

Requirements and compatibility
################################

Requirements
=============

Stock Python and a terminal

Target
========

Dev target to day is stock Python 2.5-7 with no requirement. In a near future, many other versions of Python.


Tested on
==========

This works on Python 2.7/Linux.

.. TODO

Concept
#########

This is meant to be 'easy' to use, even for non computer scientists and
required to work well even on very minimal exotic platforms such as Windows
console terminals.

Why use this
==============

The light from the most beautiful nebulae far up in the sky travels a long
time to reach us; likewise, it may be that a lot of computational time
separates you from the contemplation of an interesting result after you fed
a program heaps of data (for instance, modelisation with scikit-learn_).

It is good practice to impress the viewer with details about what's going on:
informative messages and/or progress information.
The purpose of this Python module is to help you do so.

.. _scikit-learn: http://scikit-learn.org

Feature: logging, a simpler API
================================

Some things are deliberately different from logging (however, the logging API is available). This module will
be logging to stdout by default.

Loggers defined here here have a verbosity setting: this integer has the opposite
meaning of the "log level" from logging.

Feature: Progress information
==============================

All indicators below shown can be combined at will.

Running distance unknown
~~~~~~~~~~~~~~~~~~~~~~~~~~

If your program is looping in the dark, searching for a solution with the loop
number unknown, then maybe the best output you can do to say "hey, I'm alive,
I'm digging that mine out" is a plain old dot every given number of steps::

        .


Then, one minute later, another dot::

        ..


Many dots, and so on, you get it.

There is also a counter, that you can combine with dots::

        ..........
        [Exciting computation] Iteration 1000 done
        ..........
        [Exciting computation] Iteration 2000 done
        ...

Every logger can use a different dot character if you wish::

        .....x..x....xxx..


Running distance known
~~~~~~~~~~~~~~~~~~~~~~~

It's fair, if you know your program is going to run through 42195 iterations a
particular loop, to let the viewer know how far it's gone, proportionnaly::

        [Exciting computation] 10 %
        [Exciting computation] 20 %
        ...

You can also mix this with dots.

This uses the plain logging system.

Logging and progress combined
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The combination of logging full lines and progress dots that are not
individually followed with a newline character involves a trick to end the line
before an informative message.


How to use
#############

Basic usage
============

Everything you need to read to get started.

Boilerplate
~~~~~~~~~~~~

After importing, you have to define one or several loggers with explicite names.

.. code-block:: python

    from monologue import get_logger
    logger = get_logger("explicite name")

Drop in replacement for ``print``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of

.. code-block:: python

    print "Message I intend to convey"

use

.. code-block:: python

    logger.msg("Message I intend to convey")


.. TODO
.. The following ``sed`` one liner will replace print statements with a call to ``logger.msg`` in a Python source file. It will however not handle multiline ``print`` statements properly::

Spit (custom) dots on demand
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See the calls to ``logger.dot`` in this example:

.. code-block:: python

    def fly_to_1(x):
        """
        Given x an positive integer, the loop in this function is
        believed to stop (but there is no math proof of this yet).
        """

        while x != 1:
            # Simplest way to indicate loops:
            logger.dot()

            # Display intermediate results:
            logger.dot(dot_string='[%d]' % x)

            if x % 2 == 0:  # if x is odd
                x /= 2  # halve x
            else:
                x = 3 * x + 1


Set an alternate char or string for use as dot
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Normally, you'd get plain dots:

.. code-block:: python

    for i in xrange(5):
        logger.dot()

gives::

    .....

whereas

.. code-block:: python

    logger.set_dot_str("x")
    for i in xrange(5):
        logger.dot()

gives::

    xxxxx


Mixing dots and messages
~~~~~~~~~~~~~~~~~~~~~~~~~~

Of course you can mix dots and informative messages.
This code

.. code-block:: python

    for x in xrange(10):
        logger.dot()
        if x == 5:
            logger.msg("x is 5!")

produces::

    xxxxxx
    [explicite name] x is 5!
    xxxx

Automatic progress notification (with dots and messages)
===========================================================

You can delegate the count of iterations to the logger.
For instance, let's rewrite ``fly_to_1``.

.. code-block:: python

    # Configure: a dot every 10 steps
    logger.dot_every(10)

    # Configure: progress message every 100 steps
    logger.progress_every(100)

    # Optional: reset the number of iterations
    logger.progress_reset()

    while x != 1:

        # count one step
        logger.step()

        if x % 2 == 0:  # if x is odd
            x /= 2  # halve x
        else:
            x = 3 * x + 1

    logger.complete()

If you know how many batches you are going to handle, you can even provide the user with progress percentages.

.. TODO

Logger creation, fetching and configuration
============================================

Logger uniqueness
~~~~~~~~~~~~~~~~~~

Alike to the Python *logging* API, loggers are created or fetched upon a call to ``get_logger`` (``getLogger`` in logging).
Unique loggers are identified with their names, and parametrized upon creation, ie the first call to ``get_logger`` with a given name.

Here, ``a`` and ``b`` identify the same object:

.. code-block:: python

    a = get_logger("name")
    b = get_logger("name")

Caveat: no reparametrization upon further calls to ``get_logger``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Many caracteristics of a logger can be configured upon the creation of a logger, by using optional keywords when calling ``get_logger``; however, later calls with a given logger name will only return a reference to a previously created logger.

It may be a good practice to use different thematic loggers, with different names, in different source files, or even in functions.

Specify log files (including stdout)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*monologue* can log to arbitrary places.

``logfile`` keyword
.....................

If no ``logfile`` keyword is specified to the first call to ``get_logger`` with a given name, the output defaults to ``sys.stdout``, making *monologue* a drop-in replacement for ``print``.

``logfile`` can be either:

* a file handler open for writing
* a filename, that will be open in *append* mode.

``add_logfile`` method
........................

Partial log: messages or dots only
....................................

Add a timestamp to messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Lazy formatting of messages
~~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a feature of ``logging``: a message that is not displayed because its importance does not match the verbosity of the logger will not be formatted at all.
In order to benefit from this optimization, replace

.. code-block:: python

    logger.msg("This message is about %s" % subject)

by

.. code-block:: python

    logger.msg("This message is about %s", msgvars=subject)

or

.. code-block:: python

    logger.msg("This %(adjective)s message is about %(subject)s" %
        {'adjective': 'dumb', 'subject': subject})

by

.. code-block:: python

    logger.msg("This %(adjective)s message is about %(subject)s",
        msgvars={'adjective': 'dumb', 'subject': subject})

Verbosity control
~~~~~~~~~~~~~~~~~~

Verbosity (criticity) of a message
..................................

.. TODO

Verbosity threshold of a logger
.................................

.. TODO

Roadmap
########

- handle several file descriptors for logging? also, maybe some with
  progress info, some others without.
- easy access to a log format that includes timestamp
        with an on/off switch and strptime format
- Color_?
    Also look for a Windows solution.
- Log rotation?
- A ``ProgressAndLog.child`` method?
  Such a child would be a logger with the configuration of its parent (log files and so on), but a different name.
- Setup verbosity per logfile?
- Use configuration files?
    For some of the above features.

.. _Color:
   http://stackoverflow.com/questions/384076/how-can-i-make-the-python-logging-output-to-be-colored


How to dev / contribute
#######################

Tell me if anything could be done better to suit you.

Code is developped on github: https://github.com/joblib/ ::

        git clone https://github.com/joblib/joblib.git

(will be, actually. we're still on our own in monologue)

Follow good practices.

Main gotcha, in testing, is that the default output is stdout.

- We could replace sys.stdout within the process... and experience problems with the testing framework because it also tries to use sys.stdout
- or use doctest, the path chosen until now.

From ideas to bytes (official history)
########################################

Code monkey is Feth Arezki. Packaging by Nelle Varoquaux.

The idea behind this, and many ideas of how it should be done are Gael
Varoquaux's.  Also participated in the discussion, or motivated me: Olivier
Grisel, Fabian Pedregosa, Nelle Varoquaux. See
https://github.com/scikit-learn/scikit-learn/pull/130
