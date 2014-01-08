#!/usr/bin/env python
#coding=utf-8

import config
from collections import deque


class Queue(object):

    def __init__(self):
        self.q = deque()

    def push(self, jsonjob):
        self.q.appendleft(jsonjob)
        return True

    def rpush(self, jsonjob):
        self.q.append(jsonjob)
        return True

    def lpush(self, jsonjob):
        self.q.appendleft(jsonjob)
        return True

    def rpushmany(self, *jsonjob):
        self.q.append(jsonjob)
        return True

    def lpushmany(self, *jsonjob):
        self.q.appendleft(*jsonjob)
        return True

    def rpop(self):
        try:
            return self.q.pop()
        except IndexError:
            return None

    def lpop(self):
        try:
            return self.q.pop()
        except IndexError:
            return None

    def getjobs(self, limit=None):
        jobs = [self.rpop() for i in xrange(limit or config.POP_TIMES)]
        return filter(None, jobs)

    def get(self, index):
        try:
            job = self.q[index]
        except IndexError:
            job = None
        return job

    def pack(self, url, **kw):
        job = {'url': url}.update(kw)
        return job


if __name__ == '__main__':
    q = Queue()
    for i in xrange(1, 100):
        q.lpush('{"url": "%s"}' % i)
    print q.getall()
    print q.getjobs()
    print q.get(1)
