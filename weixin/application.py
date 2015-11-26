# -*-coding:utf-8 -*-
"""
Created on 11/17/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import unicode_literals

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from hello.handlers import Hello
from docking.handlers import Entry

from tornado.options import define, options
define('port', default=8000, help='run on the given port.', type=int)


class WeixinApplication(tornado.web.Application):
    """
    The main application class of DWeixin.
    """

    def __init__(self):
        handlers = [
            (r"/", Hello),
            (r"/entry/(\w+)", Entry),
        ]

        settings = dict(
            template_path='templates',
            static_path='../static/'
        )

        super(WeixinApplication, self).__init__(handlers, **settings)


if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(WeixinApplication())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
