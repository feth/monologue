****************************
Quick features presentation
****************************

================================
Feature: logging, a simpler API
================================

Some things are deliberately different from logging (however, the logging API is available). This module will
be logging to stdout by default.

Loggers defined here here have a verbosity setting: this integer has the opposite
meaning of the "log level" from logging.

==============================
Feature: Progress information
==============================

All indicators below shown can be combined at will.


Running distance unknown
-------------------------

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
----------------------

It's fair, if you know your program is going to run through 42195 iterations a
particular loop, to let the viewer know how far it's gone, proportionnaly::

        [Exciting computation] 10 %
        [Exciting computation] 20 %
        ...

You can also mix this with dots.

This uses the plain logging system.

==============================
Logging and progress combined
==============================

The combination of logging full lines and progress dots that are not
individually followed with a newline character involves a trick to end the line
before an informative message.
