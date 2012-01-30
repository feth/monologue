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

How to dev / contribute / complain
###################################

Tell :ref:`authors` if anything could be done better to suit you.

Code is developped on github: https://github.com/joblib/ ::

        git clone https://github.com/joblib/joblib.git

(will be, actually. we're still on our own in monologue)

Follow good practices.

Main gotcha, in testing, is that the default output is stdout.

- We could replace sys.stdout within the process... and experience problems with the testing framework because it also tries to use sys.stdout
- or use doctest, the path chosen until now.

