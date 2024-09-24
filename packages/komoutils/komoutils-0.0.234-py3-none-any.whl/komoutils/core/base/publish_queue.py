import asyncio
import os
from functools import wraps
from typing import List


def ensure_parent(func):
    @wraps(func)
    def inner(self, *args, **kwargs):
        if os.getpid() != self._creator_pid:
            raise RuntimeError("{} can only be called in the "
                               "parent.".format(func.__name__))
        return func(self, *args, **kwargs)

    return inner


class PublishQueue(object):
    def __init__(self):
        self._queues: List[asyncio.Queue] = []
        self._creator_pid = os.getpid()

    def __getstate__(self):
        self_dict = self.__dict__
        self_dict['_queues'] = []
        return self_dict

    def __setstate__(self, state):
        self.__dict__.update(state)

    @ensure_parent
    def register(self) -> asyncio.Queue:
        q = asyncio.Queue()
        self._queues.append(q)
        return q

    @ensure_parent
    def publish(self, val):
        for q in self._queues:
            q.put_nowait(val)
