# -*- coding: utf-8 -*-
import copy
from Jd.db import create_conn, create_database_and_tables, insert, twisted_insert, handle_error
from Jd.items import SummaryItem, CommentItem
from twisted.enterprise import adbapi
import logging

logger = logging.getLogger(__file__)


class MysqlTwistedPipeline(object):
    """使用twisted实现异步插入数据到mysql"""
    def __init__(self, dbpool):
        self.dbpool = dbpool
        # 建表
        self.dbpool.runInteraction(create_database_and_tables)

    @classmethod
    def from_settings(cls, settings):
        db_args = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DB'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool('pymysql', **db_args)
        return cls(dbpool)

    def process_item(self, item, spider):
        # 异步插入数据到mysql，如果有错误则返回exception，正确则会自动commit，不需要人为commit，也不用创建cursor
        # 使用深拷贝，将引用传递改为值传递，有些数据重复有些数据丢失（总数量不变）
        asyn_item = copy.deepcopy(item)
        if isinstance(asyn_item, CommentItem):
            # runInteraction(callable, *args)，可调用的对象以及该对象所需要的参数
            query = self.dbpool.runInteraction(twisted_insert, asyn_item, 'comment')
        elif isinstance(asyn_item, SummaryItem):
            query = self.dbpool.runInteraction(twisted_insert, asyn_item, 'summary_comment')
        # 处理异常
        query.addErrback(handle_error, asyn_item, spider)
        return asyn_item

    def close_spider(self, spider):
        self.dbpool.close()


class JdMysqlPipeline(object):
    def __init__(self):
        self.conn = create_conn()
        self.cursor = self.conn.cursor()
        create_database_and_tables(self.cursor)

    def process_item(self, item, spider):
        if isinstance(item, CommentItem):
            insert(self.conn, item, 'comment')
        elif isinstance(item, SummaryItem):
            insert(self.conn, item, 'summary_comment')

    def close_spider(self, spider):
        self.conn.close()
