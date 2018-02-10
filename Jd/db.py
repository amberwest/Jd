#! -*- coding:utf-8 -*-
import pymysql
from Jd.settings import *
import logging

# logger = logging.getLogger(__file__)

def create_conn():
    conn = pymysql.connect(host=MYSQL_HOST, user=MYSQL_PORT, password=MYSQL_PASSWORD,  port=MYSQL_PORT,
                           db=MYSQL_DB, charset='utf8')
    return conn

def create_database_and_tables(cursor):
    # 建立jingdong数据库
    # cursor.execute('CREATE DATABASE jingdong')
    # cursor.execute('use jingdong')

    # 建立comment和summary_comment两张表
    cursor.execute("""drop table comment""")
    cursor.execute("drop table summary_comment")
    comment_sql = """
    CREATE TABLE IF NOT EXISTS comment(
    id int NOT NULL auto_increment,
    pid VARCHAR (50) NOT NULL,
    title VARCHAR (200) DEFAULT NULL ,
    nick_name VARCHAR (20) NOT NULL ,
    view_count VARCHAR (10) DEFAULT NULL ,
    user_client VARCHAR (10) DEFAULT NULL ,
    is_mobile BOOLEAN DEFAULT NULL ,
    user_level_name VARCHAR (20) DEFAULT NULL ,
    user_level_id VARCHAR (10) DEFAULT NULL ,
    user_exp_value INT (20) DEFAULT NULL ,
    plus_available INT (10) DEFAULT NULL ,
    recommend VARCHAR (10) DEFAULT NULL ,
    reference_id VARCHAR (20) DEFAULT NULL ,
    reference_name VARCHAR (200) DEFAULT NULL ,
    is_top VARCHAR (10) DEFAULT NULL ,
    comment_time DATETIME NOT NULL ,
    reference_time DATETIME DEFAULT NULL ,
    content text DEFAULT NULL ,
    first_category INT (16) DEFAULT NULL ,
    second_category INT (16) DEFAULT NULL ,
    third_category INT (16) DEFAULT NULL ,
    score INT (10) DEFAULT NULL ,
    useful_vote_count INT (10) DEFAULT NULL ,
    useless_vote_count INT (10) DEFAULT NULL,
    PRIMARY KEY (id),
    UNIQUE (pid, nick_name, comment_time)
    )ENGINE=InnoDB
    """

    summary_comment_sql = """
    CREATE TABLE IF NOT EXISTS summary_comment(
    pid VARCHAR (50) NOT NULL ,
    title VARCHAR (50) DEFAULT NULL ,
    good_rate_show VARCHAR (10),
    poor_rate_show VARCHAR (10),
    average_score VARCHAR (10),
    good_count VARCHAR (10),
    default_good_count VARCHAR (10),
    general_count VARCHAR (10),
    after_count VARCHAR (10),
    poor_count VARCHAR (10),
    PRIMARY KEY (pid)
    )ENGINE=InnoDB
    """

    cursor.execute(comment_sql)
    cursor.execute(summary_comment_sql)

def twisted_insert(cursor, data, table):
    """异步"""
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = "INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE".format(
        table=table, keys=keys, values=values)
    update = ','.join([" {key} = %s".format(key=key) for key in data])
    sql += update
    try:
        cursor.execute(sql, tuple(data.values()) * 2)
        print('insert data successfully')
    except Exception as e:
        print(e)
        # logger.warning('failed to insert data', e)

def handle_error(failure, item, spider):
    # 处理异常
    # logger.warning(failure)
    print(failure)


def insert(conn, data, table):
    cursor = conn.cursor()
    keys = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    sql = """INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE""".format(
        table=table, keys=keys, values=values)
    update = ','.join([" {key} = %s".format(key=key) for key in data])
    sql += update
    try:
        cursor.execute(sql, tuple(data.values()) * 2)
        conn.commit()
        print('insert data successfully')
    except Exception as e:
        print('failed to insert data', e)
        conn.rollback()
