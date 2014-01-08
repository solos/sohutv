#!/usr/bin/env python
#coding=utf-8

import re
import encoding
import lxml.html
import lxml.html.clean


sohutv_url_match = re.compile(r'http://tv\.sohu\.com/\d{8}/n\d+.shtml|http://so\.tv\.sohu\.com/.*?html')
info_match = re.compile(r'vid\s*=\s*"(?P<vid>\d+)".*?nid\s*=\s*"(?P<nid>\d+).*?pid\s*=\s*"(?P<pid>\d+).*?cover\s*=\s*"(?P<cover>[^"]+)".*?playlistId\s*=\s*"(?P<playlistId>\d*)".*?o_playlistId\s*=\s*"(?P<o_playlistId>\d*)".*?cid\s*=\s*"(?P<cid>\d*)".*?subcid\s*=\s*"(?P<subcid>[\d;]+)".*?osubcid\s*=\s*"(?P<osubcid>[\d;]*)".*?category\s*=\s*"(?P<category>[\d;]+)".*?cateCode.*?"(?P<cateCode>[\d;]*)".*?pianhua\s*=\s*"(?P<pianhua>\d*)".*?tag\s*=\s*"(?P<tag>[^"]*)".*?tvid\s*=\s*"(?P<tvid>\d+)"', re.DOTALL)
last_match = re.compile(u'时长.*?</span>.*?con.*?>(?P<last>.*?)<', re.DOTALL)
brief_match = re.compile(u'简介.*?</span>.*?wz">(?P<brief>.*?)<', re.DOTALL)
title_match = re.compile(u'video-title">(?P<title>.*)</h1>', re.DOTALL)
pubdate_match = re.compile(u'sohu.com/(?P<pubdate>\d+)/')


cleaner = lxml.html.clean.Cleaner(
    scripts=True,
    javascript=True,
    comments=True,
    style=True,
    links=True,
    meta=True,
    page_structure=True,
    processing_instructions=True,
    embedded=True,
    frames=True,
    forms=True,
    annoying_tags=True,
    remove_tags=None,
    allow_tags=None,
    kill_tags=None,
    remove_unknown_tags=True,
    safe_attrs_only=True,
    safe_attrs=frozenset(['abbr', 'accept', 'accept-charset']),
    add_nofollow=False,
    host_whitelist=(),
    whitelist_tags=set(['embed', 'iframe']),
    _tag_link_attrs={'a': 'href', 'applet': ['code', 'object']})


def extract_links(url, source, xpath='//a[@href]'):
    urls = []
    if not source or not isinstance(source, unicode):
        return urls
    if isinstance(url, unicode):
        url = url.encode('utf8')
    try:
        absolute_content = lxml.html.make_links_absolute(source, url)
        tree = lxml.html.fromstring(absolute_content)
    except Exception, e:
        print e
        return urls
    #extract links
    elems = tree.xpath(xpath)
    urls = map(lambda a: a.attrib['href'], elems)
    return list(set(urls))


def extract_sohutv(url, source):
    urls = sohutv_url_match.findall(source)
    return list(set(urls))


def extract_links_by_regex(url, source, regex='''(?P<url>http://.*?)["']'''):
    pattern = re.compile(regex)
    return list(set(pattern.findall(source)))


def extract_content(url, source):

    cleaned = cleaner.clean_html(source)
    content = lxml.html.fromstring(cleaned).text_content()
    return content


def extract_data(url, source, xpath):
    pass


def extract_data_by_xpath(url, source, xpath):
    pass


def extract_sohutv_data_by_regex(url, source):
    try:
        last = last_match.search(source).group('last')
    except:
        last = ''
    try:
        brief = brief_match.search(source).group('brief')
    except:
        brief = ''
    try:
        title = title_match.search(source).group('title')
    except:
        title = ''
    try:
        pubdate = pubdate_match.search(url).group('pubdate')
    except:
        pubdate = '0000-00-00'
    try:
        vid, nid, pid, cover, playlistId, o_playlistId, cid, subcid, osubcid, \
            category, cateCode, pianhua, tag, tvid = \
            info_match.findall(source)[0]
    except:
        return None
    item = {
        'pubdate': pubdate,
        'vid': vid,
        'nid': nid,
        'pid': pid,
        'cover': cover,
        'playlistId': playlistId,
        'o_playlistId': o_playlistId,
        'cid': cid,
        'subcid': subcid,
        'osubcid': osubcid,
        'category': category,
        'cateCode': cateCode,
        'pianhua': pianhua,
        'tag': tag,
        'tvid': tvid,
        'title': title,
        'last': last,
        'brief': brief
    }
    return item

if __name__ == '__main__':
    import fetcher
    url = 'http://tv.sohu.com'
    url = 'http://tv.sohu.com/20131223/n392267093.shtml'
    url = 'http://tv.sohu.com/20131223/n392267093.shtml'
    status, content = fetcher.fetch(url)
    _, ucontent = encoding.html_to_unicode('', content)
    #print extract_links(url, ucontent)
    #print extract_content(url, ucontent)
    #print extract_sohutv(url, ucontent)
    print extract_sohutv_data_by_regex(url, ucontent)
