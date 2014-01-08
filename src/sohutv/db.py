#!/usr/bin/env python
#coding=utf-8

import config
import MySQLdb


def insert_item(item):
    if not item:
        return
    try:
        conn = MySQLdb.connect(
            host=config.DB_HOST,
            db=config.DB_DB,
            user=config.DB_USER,
            passwd=config.DB_PASSWORD,
            charset=config.DB_CHARSET
        )
    except Exception, e:
        print e
        return
    cursor = conn.cursor()
    try:
        cursor.execute('''insert into video(
            vid, nid, pid, cover, playlistId, o_playlistId, cid, subcid,
            osubcid, category, cateCode, pianhua, tag, tvid, pubdate) values(
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (item["vid"],
              item["nid"],
              item["pid"],
              item["cover"],
              item["playlistId"],
              item["o_playlistId"],
              item["cid"],
              item["subcid"],
              item["osubcid"],
              item["category"],
              item["cateCode"],
              item["pianhua"],
              item["tag"],
              item["tvid"],
              item["pubdate"])
        )
        conn.commit()
    except Exception, e:
        print e
    cursor.close()
    conn.close()

if __name__ == '__main__':
    pass
