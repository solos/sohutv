#!/usr/bin/env python
#coding=utf-8

import gevent
from gevent import monkey
monkey.patch_all()

import config
import requests

s = requests.Session()


def fetch(url, timeout=None, headers={}, proxy={}, user_agent=None, **kw):
    status, content = 408, ''
    timeout = timeout or config.TIMEOUT
    headers = headers or config.HEADERS
    headers["user-agent"] = user_agent or config.USER_AGENT
    if proxy:
        try:
            with gevent.Timeout(config.TIMEOUT, Exception):
                r = requests.get(url, stream=False,
                                 verify=False, timeout=timeout,
                                 headers=headers, proxies=proxy)
        except Exception, e:
            print e
            return status, content
    else:
        try:
            with gevent.Timeout(config.TIMEOUT, Exception):
                r = s.get(url, stream=False, verify=False, timeout=timeout,
                          headers=headers)
        except Exception, e:
            print e
            return status, content
    return r.status_code, r.content

if __name__ == '__main__':
    url = 'http://www.baidu.com'
    print fetch(url)
