"""
Small example showing recursive logging in an object hierarchy.
"""

from time import sleep
import itertools

from monologue import get_logger
from monologue.core import ProgressAndLog

FIRST_NAMES = itertools.cycle(['Jane', 'Joe', 'Jack'])

class BaseClass(object):

    def _get_logger(self):
        if isinstance(self.verbose, ProgressAndLog):
            return self.verbose
        return get_logger(name=self.__class__.__name__,
                          verbosity_offset=self.verbose)


class Employee(BaseClass):

    def __init__(self, name='Joe Average', verbose=False):
        self.name = name
        self.verbose = verbose

    def work(self, chore_msg):
        log = self._get_logger()
        sleep(.2)
        log.msg('%s says "Done my chores %s"',
                msgvars=(self.name, chore_msg))


class Boss(BaseClass):

    def __init__(self, n_employees=3, verbose=False):
        self.verbose = verbose
        self.n_employees = n_employees


    def yell(self):
        log = self._get_logger()
        log.msg('Get to work!!')
        employes = [Employee(name='%s Average' % n,
                            verbose=log.clone())
                    for n, _ in zip(range(self.n_employees),
                                 FIRST_NAMES)]

        for employe in employes:
            employe.work()


if __name__ == '__main__':
    boss = Boss()
    boss.yell()
