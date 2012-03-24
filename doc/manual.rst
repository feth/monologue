#############
API Manual
#############

****************
Getting started
****************

============
Boilerplate
============

After importing, you have to define one or several loggers with explicit names.

.. code-block:: python

    from monologue import get_logger
    logger = get_logger("explicit name")

==================================
Drop in replacement for ``print``
==================================

Instead of

.. code-block:: python

    print "Message I intend to convey"

use

.. code-block:: python

    logger.msg("Message I intend to convey")


.. TODO
.. The following ``sed`` one liner will replace print statements with a call to ``logger.msg`` in a Python source file. It will however not handle multiline ``print`` statements properly::

Spit (custom) dots on demand
----------------------------------

See the calls to ``logger.dot`` on lines 13 and 16 of this example:

.. code-block:: python
    :linenos:
    :emphasize-lines: 13, 16

    def fly_to_1(x):
        """ Given x an positive integer, the loop in this function is
        believed to stop (but there is no math proof of this yet).  """

        while x != 1:

            if x % 2 == 0:  # if x is odd
                x /= 2  # halve x
            else:
                x = 3 * x + 1

            # Simplest way to indicate loops:
            logger.dot()

            # Display intermediate results:
            logger.dot(dot_string='[%d]' % x)

Set an alternate char or string for use as dot
-----------------------------------------------

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
--------------------------

Of course you can mix dots and informative messages.
This code

.. code-block:: python

    for x in xrange(10):
        logger.dot()
        if x == 5:
            logger.msg("x is 5!")

produces the following output::

    xxxxxx
    [explicit name] x is 5!
    xxxx

***************
More in depth
***************

==========================================================
Automatic progress notification (with dots and messages)
==========================================================

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

==============================================
Logger creation, fetching and configuration
==============================================

.. TODO

Logger uniqueness
--------------------

Alike to the Python *logging* API, loggers are created or fetched upon a call to ``get_logger`` (``getLogger`` in logging).
Unique loggers are identified with their names, and parametrized upon creation, ie the first call to ``get_logger`` with a given name.

Here, ``a`` and ``b`` identify the same object:

.. code-block:: python

    a = get_logger("name")
    b = get_logger("name")

Caveat: no reparametrization upon further calls to ``get_logger``
-------------------------------------------------------------------

Many caracteristics of a logger can be configured upon the creation of a logger, by using optional keywords when calling ``get_logger``; however, later calls with a given logger name will only return a reference to a previously created logger.

It may be a good practice to use different thematic loggers, with different names, in different source files, or even in functions.

Specify log files (including stdout)
------------------------------------

*monologue* can log to arbitrary places.

.. _logfile_keyword:

``logfile`` keyword of ``get_logger``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If no ``logfile`` keyword is specified to the first call to ``get_logger`` with a given name, the output defaults to ``sys.stdout``, making *monologue* a drop-in replacement for ``print``.

``logfile`` can be either:

* a file handler open for writing
* a filename, that will be open in **append** mode.

``add_logfile`` method of ``ProgressAndLog``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. TODO

Partial log: messages or dots only
----------------------------------

Add a timestamp to messages
----------------------------

Lazy formatting of messages
----------------------------

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
-------------------

Verbosity (criticity) of a message
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. TODO

Verbosity threshold of a logger
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. TODO
