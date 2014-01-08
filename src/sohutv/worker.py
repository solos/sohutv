#!/usr/bin/env python
#coding=utf-8

from gevent import monkey
monkey.patch_all()
from gevent.pool import Pool

import db
import json
#import queue
import redisqueue as queue
import config
import fetcher
import encoding
import extracter
from logger import logger

gpool = Pool(config.GPOOLSIZE)


def work():
    #q = queue.Queue()
    q = queue.RedisQueue()
    q.lpush('{"url": "http://tv.sohu.com"}')
    jobs = q.getjobs()
    while jobs:
        for job in jobs:
            print 'job', job
            gpool.spawn(handle, job, queue=q)
        gpool.join()
        jobs = q.getjobs()


def handle(job, *args, **kwargs):
    queue = kwargs['queue']
    task = json.loads(job)
    url = task["url"]
    status, source = fetcher.fetch(url, use_proxy=False)
    logger.info('%s|%s' % (url, status))
    try:
        _, ucontent = encoding.html_to_unicode('', source)
    except Exception, e:
        print e
    item = extracter.extract_sohutv_data_by_regex(url, ucontent)
    db.insert_item(item)
    urls = extracter.extract_sohutv(url, source)
    for i in urls:
        if queue.check_fetched(config.BITMAP, i):
            continue
        queue.lpush('{"url": "%s"}' % i)
    return urls

if __name__ == '__main__':
    work()
