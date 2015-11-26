# -*-coding:utf-8 -*-
"""
Created on 11/19/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import unicode_literals

import sys
import bcrypt

import tornado.gen

import settings
from utils.db import db_pool
from exception.db import ObjectNotExists, MultipleObjectsReturned
from core.models import SingleObjectModel

if not sys.version_info[0] == 2:
    unicode = str


class User(SingleObjectModel):
    """
    The User Model Class for quick query.
    """

    db_table = 'user_user'
    fields = ['id', 'username', 'email', 'password', 'is_superuser', 'is_staff', 'is_active', 'last_login',
              'date_joined', 'login_attempted', 'updated', 'secret', 'verification_needed']

    def gen_password(self, raw_password, salt=None):
        p = '$'.join([raw_password, settings.secret_key])
        return bcrypt.hashpw(p.encode('utf8'), salt or bcrypt.gensalt())

    @tornado.gen.coroutine
    def check_password(self, raw_password):
        if self.data:
            hashed_password = self.data.get('password')
        else:
            sql = "SELECT password FROM `user_user` WHERE {0}"

            cursor = yield db_pool.execute(sql.format(self.queries))
            res = cursor.fetchall()
            if not res:
                raise ObjectNotExists
            elif len(res) > 1:
                raise MultipleObjectsReturned
            hashed_password = res[0][0]

        hashed_password = hashed_password.encode('utf8')
        raise tornado.gen.Return(True if self.gen_password(raw_password, hashed_password) == hashed_password else False)
