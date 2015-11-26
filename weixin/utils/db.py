# -*-coding:utf-8 -*-
"""
Created on 11/19/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import print_function, unicode_literals

from tmysql import pools

import settings

pools.DEBUG = True


db_pool = pools.Pool(settings.mysql_db.get('config'), **settings.mysql_db.get('connection'))
