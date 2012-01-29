###########
About this
###########

********************
License information
********************

.. compound::

    .. include:: COPYING

*******
Concept
*******

*monologue* is built with ease of use in mind, especially for non
software engineers; and works well even on very minimal exotic platforms
such as Windows console terminals.

**********************************
Why you should be using monologue
**********************************

The light from the most beautiful nebulae far up in the sky travels a long
time to reach us; likewise, it may be that a lot of computational time
separates you from the contemplation of an interesting result after you fed
a program heaps of data (for instance, modelisation with scikit-learn_).

It is good practice to impress the viewer with details about what's going on:
informative messages and/or progress information.
The purpose of this Python module is to help you do so.

If you use *monologue*, which is not a burden, your code will be more
reusable, more embeddable!

.. _scikit-learn: http://scikit-learn.org

****************************************
From ideas to bytes (official history)
****************************************

Code monkey is :ref:`Feth Arezki`. Packaging by Nelle Varoquaux.

The idea behind this, and many ideas of how it should be done are Gael
Varoquaux's.  Also participated in the discussion, or motivated me: Olivier
Grisel, Fabian Pedregosa, Nelle Varoquaux. See
https://github.com/scikit-learn/scikit-learn/pull/130

****************************
Quick features presentation
****************************

================================
Feature: logging, a simpler API
================================

The loggers provided by *monologue* are preconfigured so as to
fit your needs with the least boilerplate possible: you can start
using them as cute drop-in replacements for the ``print`` statements,
and later fine tune the logging behaviour to specific needs (log to
-several- files, laconic to verbose logs...).

==============================
Feature: Progress information
==============================

There are several progress indicators for loop based computations,
and they can be combined at will.

Mainly, there are two usecases: whether the number of steps is known in
advance or not.

* progress indicators on a single line every given number of steps
    (``dot`` method):

    With an indefinite number of loops to go through, this is maybe the
    best output your program can do to say "hey, I'm alive, I'm digging
    that mine out".

    In the simplest form, it looks like this::

        .......

    We can also output arbitrary strings, such as::

        ...XX......XXXXX........

    Or display arbitrary intermediate indicators::

        [4][5][9][1]

    If you do a parallel computation, you may want to assign a different
    character to each processing unit::

        caacbbababbbabaaaacaaaccbabaaccabbbbcccbbc

* automatic counter, also every given number of steps (configure with
    ``progress_every`` method):

    Like dots, a counter is relevant when the number of steps is not
    known in advance::

        [Exciting computation] Iteration 1000 done
        [Exciting computation] Iteration 2000 done

    Transparently combined with the dot feature::

        ..........
        [Exciting computation] Iteration 1000 done
        ..........
        [Exciting computation] Iteration 2000 done
        ...

* End of computation (``progress_complete`` method):

    Your program might conveniently display an *end of computation*
    message::

        [Exciting computation] Successfully completed 2435 iterations


* Progress percentage (configure with ``percent_every`` method)

    It's fair, if you know your program is going to run a particular
    loop 42195 times to let the viewer know how far it's gone,
    proportionnaly::

        [Exciting computation] 10 %
        [Exciting computation] 20 %
