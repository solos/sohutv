#!/usr/bin/env python
#coding=utf-8

import redis
import config
import murmur

POOL = redis.ConnectionPool(host=config.RHOST,
                            port=config.RPORT,
                            db=config.RDB)


class RedisQueue(object):

    def __init__(self):
        self.r = redis.Redis(connection_pool=POOL)

    def rpush(self, jsonjob, queue=config.QUEUE):
        try:
            self.r.rpush(queue, jsonjob)
        except Exception, e:
            print e
            return False
        return True

    def lpush(self, jsonjob, queue=config.QUEUE):
        try:
            self.r.lpush(queue, jsonjob)
        except Exception, e:
            print e
            return False
        return True

    def rpop(self, queue=config.QUEUE):
        try:
            self.r.rpop(queue)
        except Exception, e:
            print e
            return None

    def lpop(self, queue=config.QUEUE):
        try:
            self.r.lpop(queue)
        except Exception, e:
            print e
            return None

    def check_fetched(self, bitmap, url):
        mhash = murmur.string_hash(url)
        if self.r.getbit(bitmap, mhash):
            return True
        else:
            self.r.setbit(bitmap, mhash, 1)
            return False

    def getjobs(self, queue=config.QUEUE, limit=None):
        jobs = [self.r.rpop(queue) for i in xrange(limit or config.POP_TIMES)]
        return filter(None, jobs)


if __name__ == '__main__':
    pass
