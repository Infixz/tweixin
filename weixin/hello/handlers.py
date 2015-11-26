# -*-coding:utf-8 -*-
"""
Created on 11/17/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import unicode_literals

import tornado.gen
import tornado.web
from docking.utils.menu import init_selfmenu_info

from docking.utils.token import get_access_token
from docking.models.config import Account

from core.storage import storage
from user.models import User


class Hello(tornado.web.RequestHandler):
    """
    Say hello to you.
    """

    f = None
    l = 0

    def get(self, *args, **kwargs):
        self.write('Welcome to Tornado!')

    @tornado.gen.coroutine
    def check_password(self, *args, **kwargs):
        res = yield User(id=1).check_password('123466')

        self.write('PASSED.' if res else 'DENIED.')
        self.finish()

    @tornado.gen.coroutine
    def get_access_token(self, *args, **kwargs):
        account = yield Account(id=1).get()
        res = yield get_access_token(account)
        self.write(res)

    def upload(self, *args, **kwargs):
        paths = []
        for key, ufs in self.request.files.items():
            for uf in ufs:
                paths.append(storage.save(uf.get('filename'), uf.get('body')))

        self.write(', '.join(paths))

    @tornado.gen.coroutine
    def flush_selfmenu(self, *args, **kwargs):
        account = yield Account(id=1).get()
        yield init_selfmenu_info(account=account)
        self.write('OK.')

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        t = self.get_argument('type', '')
        if t == 'u':
            self.upload(*args, **kwargs)
        elif t == 'a':
            yield self.get_access_token(*args, **kwargs)
        elif t == 'p':
            yield self.check_password(*args, **kwargs)
        elif t == 'm':
            yield self.flush_selfmenu(*args, **kwargs)
        else:
            self.write('WELCOME TO TEST HANDLER.')
