import psutil
import time

from config import ignore_users, ignore_names
from db.dbHandler import DbHandler


class ProcessMonitor:
    def __new__(cls, *args, **kwargs):
        if not hasattr(ProcessMonitor, '__instance'):
            setattr(ProcessMonitor, '__instance', super(ProcessMonitor, cls).__new__(cls))
        return getattr(ProcessMonitor, '__instance')

    def __init__(self):
        self.__ignore_users = ignore_users
        self.__ignore_names = ignore_names

    def _get_processes(self):
        not_ignore = lambda p: p.info['username'] not in self.__ignore_users \
                               and p.info['name'] not in self.__ignore_names \
                               and p.cpu_percent() > 10
        return [p.info['name'] for p in psutil.process_iter(attrs=['name', 'username']) if not_ignore(p)]

    @staticmethod
    def _update_durations(procs: list, interval: float):
        db_handler = DbHandler()
        for pname in procs:
            db_handler.inc_process_duration(pname, interval)

    def monitor(self):
        cur = time.time()
        while True:
            procs = self._get_processes()
            ProcessMonitor._update_durations(procs, cur - time.time())
            cur = time.time()
            time.sleep(2)
