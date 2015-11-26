# -*-coding:utf-8 -*-
"""
Created on 11/20/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import unicode_literals

import sys
import datetime

import tornado.gen

from utils.db import db_pool
from exception.db import ObjectNotExists
from tmysql import escape_string

if not sys.version_info[0] == 2:
    unicode = str


class SingleObjectModel(object):

    db_table = ''
    fields = ['id']
    defaults = None
    data = None
    order_by = None
    query = None

    def __init__(self, **queries):
        super(SingleObjectModel, self).__init__()

        self.queries_raw = queries

        parsed = []
        defaults = self.defaults or {}
        for k, v in queries.items():
            v = self.to_string(v) if v is not None else defaults.get(k)
            v = v() if callable(v) else v
            parsed.append("`{0}`={1}".format(k, v))

        self.queries = ' AND '.join(parsed)

    def to_string(self, raw):
        if isinstance(raw, (datetime.datetime, datetime.date)):
            raw = raw.strftime('%Y-%m-%d %H:%M:%S')

        if isinstance(raw, (str, unicode)):
            return "'{0}'".format(escape_string(raw))
        elif isinstance(raw, int):
            return "{0}".format(raw)

        return str(raw)

    @tornado.gen.coroutine
    def _filter(self):
        sql = "SELECT {0} FROM `{1}` WHERE {2}"
        if self.order_by:
            order_by = []
            for o in self.order_by:
                order_by.append("`{0}` DESC".format(o[1:]) if o.startswith('-') else "`{0}` ASC".format(o))
            sql += " ORDER BY {0}".format(', '.join(order_by))

        self.query = sql.format(', '.join(['`{0}`'.format(f) for f in self.fields]), self.db_table, self.queries)
        print(self.query)
        cursor = yield db_pool.execute(self.query)
        raise tornado.gen.Return(cursor)

    @tornado.gen.coroutine
    def get(self):
        cursor = yield self._filter()

        res = cursor.fetchone()
        if not res:
            raise ObjectNotExists

        self.data = dict(zip(self.fields, res))

        raise tornado.gen.Return(self)

    @tornado.gen.coroutine
    def filter(self):
        cursor = yield self._filter()
        self.fetch_method = cursor.fetchone

        raise tornado.gen.Return(self)

    def __iter__(self):
        return self

    def __next__(self):
        res = self.fetch_method()
        if res:
            self.data = dict(zip(self.fields, res))
            return self
        raise StopIteration

    @tornado.gen.coroutine
    def get_or_create(self, **restrictions):
        sql_base = "INSERT INTO `{table_name}` ({fields}) " \
                   "SELECT {values} FROM DUAL " \
                   "WHERE NOT EXISTS (SELECT id FROM `{table_name}` WHERE " \
                   "{restrictions}) LIMIT 1"

        defaults = self.defaults or {}
        fields = []
        values = []
        for f in self.fields:
            if f == 'id':
                continue
            fields.append('`{0}`'.format(f))
            v = self.queries_raw.get(f)
            v = defaults.get(f) if v is None else v
            v = v() if callable(v) else v
            values.append(self.to_string(v))

        kwargs = {
            'table_name': self.db_table,
            'fields': ', '.join(fields),
            'values': ', '.join(values),
            'restrictions': ' AND '.join(["`{0}`={1}".format(k, self.to_string(v)) for k, v in restrictions.items()]) if restrictions else 'id=0'
        }
        print('SQL:', sql_base.format(**kwargs))
        yield db_pool.execute(sql_base.format(**kwargs))

        user = yield self.get()
        raise tornado.gen.Return(user)

    @tornado.gen.coroutine
    def delete(self):
        sql_base = "DELETE FROM `{0}` WHERE {1}"

        self.query = sql_base.format(self.db_table, self.queries)
        yield db_pool.execute(self.query)

    def __getattr__(self, item):
        return self.data.get(item) if self.data else None
