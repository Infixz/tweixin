# -*-coding:utf-8 -*-
"""
Created on 11/19/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import unicode_literals


secret_key = '2-^v80drsrou3vv)yyggoh^v!aco57qzs7+)nl3=ef4g6=_z^5'

mysql_db = {
    'config': {
        'host': '192.168.141.130',  # MySQL Server host.
        'port': 3306,               # MySQL Server port.
        'user': 'root',             # Login username.
        'passwd': '',               # Login password.
        'db': 'weixin2',            # Database name.
        'charset': 'utf8'           # Charset you want to use.
    },
    'connection': {
        'max_idle_connections': 2,  # Max number of keeping connections.
        'max_recycle_sec': 3600,    # How long connections are recycled.
        'max_open_connections': 0   # Max number of opened connections. 0 means no limit.
    }
}

media_url = '/media/'
media_root = '../media/'
