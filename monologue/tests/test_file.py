from monologue import get_logger
from tempfile import mkdtemp, mkstemp
import nose
import os
import sys

def test_stdout_init():
    logger = get_logger("test.stdout_init", logfile=sys.stdout)
    assert logger

def _log_sequence(logger):
    logger.dot_every(2)
    logger.set_dot_string("x")
    logger.msg("hello 1")
    logger.msg("hello 2")
    for time in xrange(100):
        logger.progress_step()
    logger.progress_complete()
    logger.msg("hello 3")

_LOG = 0
_DOTS = 1
_EXPECTED = ((_LOG, "[%(logger_name)s] hello 1"),
        (_LOG, "[%(logger_name)s] hello 2"),
        (_DOTS, "x"*50),
        (_LOG, "[%(logger_name)s] Successfully completed 100 iterations"),
        (_LOG, "[%(logger_name)s] hello 2"))

def _expected(logger_name, logs=True, dots=True):
    """
    generates expected logged lines if you ran your logger through _log_sequence
    """
    for line in _EXPECTED:
        line_type, text = line
        display = (line_type == _LOG and logs) or (line_type == _DOTS and dots)
        if display:
            yield text % {'logger_name': logger_name}

def _check_logfile(filename, logger_name, logs=True, dots=True):
    with open(filename, 'r') as fdesc:
        expected = _expected(logger_name)
        for line in fdesc:
            line == expected.next()
    nose.tools.assert_raises(StopIteration, expected.next)

def test_fdesc():
    """
    todo: use setup to create initial file desc and teardown to unlink it
    """
    fdesc, filename = mkstemp(suffix='.log')
    # FIXME: how do you use that fdesc? It's an int.
    fdesc = open(filename, 'wb')
    logger = get_logger("test.fdesc", logfile=fdesc)

    _log_sequence(logger)

    fdesc.close()

    _check_logfile(filename, "test.fdesc")

    os.unlink(filename)

def test_filename():
    directory = mkdtemp()
    filename = os.path.join(directory, "my_logfile.log")
    logger = get_logger("test.filename", logfile=filename)

    _log_sequence(logger)

    _check_logfile(filename, "test.filename")  # race if file not closed?

    os.unlink(filename)
    os.rmdir(directory)


def test_add_logfile():
    directory = mkdtemp()
    first_filename = os.path.join(directory, "first_file.log")
    second_filename = os.path.join(directory, "second_file.log")
    logger = get_logger("test.add_logfile", logfile=first_filename)
    logger.add_logfile(second_filename)

    _log_sequence(logger)

    _check_logfile(first_filename, "test.add_logfile")
    _check_logfile(second_filename, "test.add_logfile")

    os.unlink(first_filename)
    os.unlink(second_filename)
    os.rmdir(directory)
