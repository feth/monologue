==========
MONOLOGUE
==========

This Python module offers an interface to unify:

- logging
- marking of processing progression with dots.


.. contents::

.. sectnum::


Licence
========

See COPYING: New BSD licence (open to discussion).

Requirements and compatibility
==============================

.. TODO

Target to day is stock Python 2.7 with no requirement.

Here be moreinfo.

Concept
=========

This is meant to be 'easy' to use, even for non computer scientists and
required to work well even on very minimal exotic platforms such as Windows
console terminals.

Even the light from the most beautiful nebulae far up in the sky needs some
time to reach us, so do the results of some scikit-learn based calculations;
it's a good practice to impress the user with details about what's going on
(informative messages -we use traditional Python logging for that) and/or
progress information.

Differences with stock logging
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some things are deliberately different from logging.  This will be logging to
stdout by default. You can log somewhere else, but that's optional.

In monologue, there is a verbosity setting; that integer has the opposite meaning of the "log level" from logging.

Progress information
~~~~~~~~~~~~~~~~~~~~~~~

Running distance unknown
-------------------------------

If your program is looping in the dark, searching for a solution with the loop
number unknown, then maybe the best output you can do to say "hey, I'm alive,
I'm digging that mine out" is a plain old dot::

        .


Then, one minute later, another dot::

        ..


Many dots, and so on, you get it.


Running distance known
-------------------------------

It's fair, if you know your program is going to run through 42195 iterations a
particular loop, to let the viewer know how far it's gone (at configurable
milestones)::

        [Exciting computation] Progress: 2.36 %
        [Exciting computation] Progress: 4.72 %
        ...


How to use
===========

Here be docs

.. TODO

From brain to bytes
======================

The idea behind this, and many ideas of how it should be done are Gael Varoquaux's.
Also participated in the discussion, or motivated me:
Olivier Grisel, Fabian Pedregosa, Nelle Varoquaux. See
https://github.com/scikit-learn/scikit-learn/pull/130

