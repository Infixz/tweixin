# -*-coding:utf-8 -*-
"""
Created on 11/23/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import unicode_literals

import sys

if sys.version_info[0] == 3:
    from urllib.parse import urlencode
else:
    from urllib import urlencode

import tornado.gen
import tornado.httpclient


@tornado.gen.coroutine
def request_async(url, params, method='GET', data=None):
    """
    Request a url and fetch response asynchronously.

    :param url: URL to be requested.
    :return: tornado.gen.Return Instance with the response body.
    """

    client = tornado.httpclient.AsyncHTTPClient()

    kwargs = {
        'request': url + '?' + urlencode(params),
        'method': method,
    }
    if method == 'post' and data and isinstance(data, dict):
        kwargs['body'] = urlencode(data)

    response = yield tornado.gen.Task(client.fetch, **kwargs)

    raise tornado.gen.Return(response.body)
