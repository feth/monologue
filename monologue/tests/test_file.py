from monologue import get_logger
from tempfile import mkstemp
import sys

def test_stdout_init():
    logger = get_logger("test.stdout_init", logfile=sys.stdout)
    assert logger

def test_tmpfile():
    fdesc, filename = mkstemp(suffix='.log')
    # FIXME: how do you use that fdesc? It's an int.
    fdesc = open(filename, 'wb')
    logger = get_logger("test.tmpfile", logfile=fdesc)
    assert logger
    logger.dot_every(2)
    logger.set_dot_string("x")
    logger.msg("hello 1")
    logger.msg("hello 2")
    for time in xrange(100):
        logger.progress_step()
    logger.progress_complete()
    logger.msg("hello 3")

    fdesc.close()

    with open(filename, 'r') as fdesc:
        file_content = fdesc.read()
        file_expected = """[test.tmpfile] hello 1
[test.tmpfile] hello 2
xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
[test.tmpfile] Successfully completed 100 iterations
[test.tmpfile] hello 3
"""
    assert file_content == file_expected, "expected: "\
        "<<\n%s\n>> and got <<\n%s\n>>" % (file_content, file_expected)


