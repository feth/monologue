==========
MONOLOGUE
==========

Autotest status
----------------
.. image:: https://secure.travis-ci.org/feth/monologue.png?branch=master

See why: http://travis-ci.org/#!/feth/monologue

Supported Python
----------------

* Python 2.6,
* Python 2.7,
* Python 3.2

Dependencies
------------

::

        None

What is this
------------

A single file module that handles logging and progress information.

.. custom role to bypass the sphinx ref directive
.. role:: ref

Main documentation
------------------

http://feth.github.com/monologue/

(Not sure it's the latests build: it's a pain, building for github).

.. include:: doc/whatsthis.rst

.. include:: doc/requirements.rst

.. include:: doc/about.rst

Status
------

Don't use yet, unless you know what you're doing, because this is what's left to do:

* complete docstrings and doc; comply to joblib's doc style.
* maybe discuss some API improvements
  * why not make a ProgressAndLog.progress member to hold all accessors regarding progress?
  * maybe think of the same for log files.
  * maybe some methods/attrs renaming should occur.
