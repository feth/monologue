from tempfile import mkdtemp
from monologue import get_logger
import nose
import os


def test_with_time():
    directory = mkdtemp()
    logfile = os.path.join(directory, "log_with_time.log")
    logger = get_logger("test.with_time", logfile=logfile, timestamp=True)
    logger.msg("log_with_date")
    with open(logfile, 'r') as fdesc:
        content = fdesc.read()
    nose.tools.assert_regexp_matches(content,
            '\[.*\]\[test.with_time\] log_with_date\n')
    # TODO: better regex, or use datetime to parse the match
