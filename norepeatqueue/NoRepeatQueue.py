# ! /usr/bin/env python
# -*- coding: utf-8 -*-
import Queue
from Link import Link
class NoRepeatQueue(Queue.Queue):
    def _init(self,maxsize=0):
        self.queue = Link()

    def _put(self, item):
        self.queue.add(item)

    def _qsize(self, len=len):
        return self.queue.__len__()

    def _get(self):
        return self.queue.pop()

