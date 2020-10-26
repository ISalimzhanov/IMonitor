import time

from redis import Redis
import datetime


class DbHandler:
    def __new__(cls, *args, **kwargs):
        if not hasattr(DbHandler, '__instance'):
            setattr(DbHandler, '__instance', super(DbHandler, cls).__new__(cls))
        return getattr(DbHandler, '__instance')

    def __init__(self):
        self.redis = Redis(db=10)

    def inc_process_duration(self, pname: str, interval: float) -> None:
        self.redis.hincrbyfloat('today_proc', pname, interval)

    def inc_web_duration(self, dns_name: str, interval: float) -> None:
        self.redis.hincrbyfloat('today_web', dns_name, interval)

    def _update(self) -> None:
        procs: dict = self.redis.hgetall('today_proc')
        for pname, duration in procs.items():
            self.redis.zincrby('per_day_proc', duration, pname)
            self.redis.hdel('today_proc', pname)
        web_acts: dict = self.redis.hgetall('today_web')
        for web_act, duration in web_acts.items():
            self.redis.zincrby('per_day_proc', duration, web_act)
            self.redis.hdel('today_web', web_act)
        self.redis.save()

    def launch(self) -> None:
        while True:
            cur = datetime.datetime.today()
            if cur.hour == 0 and cur.minute == 0:
                self._update()
            else:
                time.sleep(5)
