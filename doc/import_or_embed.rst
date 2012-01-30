#############################
Install or embed, then import
#############################

=====================
Standard installation
=====================

Not documented yet. There is packaging.

**TODO** if we don't get merged into another project.

================================
Embed in your project and import
================================

Embed
--------

Copy ``monologue/core.py`` in your project's main dir, perhaps changing its name to something more explicit, such as ``monologue.py``.

Import
--------

In the same package as ``monologue.py``, just do:

.. code-block:: python

    from .monologue import get_logger
