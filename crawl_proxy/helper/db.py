from crawl_proxy.custom_settings import mysql_settings

import pymysql


def get_mysql_connection():
    _db = pymysql.connect(
        host=mysql_settings['MYSQL_HOST'],
        db=mysql_settings['MYSQL_DB'],
        user=mysql_settings['MYSQL_USER'],
        passwd=mysql_settings['MYSQL_PASSWD']
    )
    return _db
