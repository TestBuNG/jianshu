# -*- coding: utf-8 -*-
import pymysql
from twisted.enterprise import adbapi
from pymysql import cursors


class JianshuSpiderPipeline(object):
    def __init__(self):
        dbparams = {
            'host': 'localhost',
            'port': 3309,
            'user': 'root',
            'password': '123456',
            'database': 'jianshu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor   
        }

        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)  
        self._sql = None #保存sql语句

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into article(id,title,content,author,avatar,pub_time,article_id,origin_url,read_count,like_count,word_count,subjects,comments_count)
            values(null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """
            return self.sql
        return self._sql

    def process_item(self, item, spider):
        defer = self.dbpool.runInteraction(self.insert_item, item)

        defer.addErrback(self.handle_error, item, spider)

    def handle_error(self, error, item, spider):
        print('='*10 + "error" + '='*10)
        print(error)
        print('='*10 + "error" + '='*10)

    def insert_item(self, cursor, item):
        cursor.execute(self.sql, (item['title'], item['content'],item['author'],
                                  item['avatar'],item['pub_time'],item['article_id'],
                                  item['origin_url'],item['read_count'],item['like_count'],
                                  item['word_count'],item['subjects'],item['comments_count']))