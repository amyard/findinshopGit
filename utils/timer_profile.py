# -*- coding: utf-8 -*-
import time


class TimerProfile(object):
    def __init__(self, name=''):
        self.name = name
        self.start = time.time()
        self.checkpoint_time = time.time()

    @property
    def elapsed(self):
        return time.time() - self.start

    @property
    def time_task(self):
        _old_time = self.checkpoint_time
        self.checkpoint_time = time.time()
        return time.time() - _old_time

    @staticmethod
    def humanize_time(secs):
        mins, secs = divmod(secs, 60)
        hours, mins = divmod(mins, 60)
        return '%02d:%02d:%02d' % (hours, mins, secs)

    def checkpoint(self, name=''):
        result = u'{timer} {checkpoint} took {time_task} \
seconds, all running time {elapsed}'.format(
            timer=self.name,
            checkpoint=name,
            time_task=self.humanize_time(self.time_task),
            elapsed=self.humanize_time(self.elapsed)).strip()
        return result

    def __enter__(self):
        return self
