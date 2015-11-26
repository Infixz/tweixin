# -*-coding:utf-8 -*-
"""
Created on 11/26/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

import json
import datetime

import tornado.gen

from .request import request_async

from docking.models.config import AccessToken
from exception.db import ObjectNotExists
from exception.request import GetAccessTokenFailed

ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'


@tornado.gen.coroutine
def flush_access_token(app_id='wx098d830462ffddf2', secret='b61bc732cde486cf6edba0dbafe09a9c'):
    """
    Flush access token.

    :param app_id: Wechat appid.
    :param secret: Wechat secret
    :return: tornado.gen.Return Instance with loaded requested json data.
    """

    params = {
        'grant_type': 'client_credential',
        'appid': app_id,
        'secret': secret
    }
    response = yield request_async(ACCESS_TOKEN_URL, params)

    try:
        data = json.loads(response.decode('utf8'))
    except (TypeError, ValueError) as e:
        raise GetAccessTokenFailed(e)

    if data.get('errcode'):
        raise GetAccessTokenFailed('{0}: {1}'.format(data.get('errcode'), data.get('errmsg')))

    raise tornado.gen.Return(data)


@tornado.gen.coroutine
def get_access_token(account):
    """
    Get access token.
    Try to get a new one if it not exists or is already expired.

    :param account: docking.models.Account instance.
    :return: tornado.gen.Return Instance with the access_token.
    """

    try:
        access_token = yield AccessToken(account_id=account.id, account_agent_id=account.account_agent_id).get()
    except ObjectNotExists:
        access_token = None

    if not access_token or (access_token.expired - datetime.datetime.now()).total_seconds() < 60:
        # Get a new one.
        new = yield flush_access_token(account.app_id, account.secret)
        print('NEW:', new)
        expired = datetime.datetime.now() + datetime.timedelta(seconds=new.get('expires_in') - 60)

        # Save to db.
        access_token = yield AccessToken(account_id=account.id,
                                         account_agent_id=account.account_agent_id,
                                         access_token=new.get('access_token'),
                                         expired=expired).get_or_create(expired=expired)
    # Return the access_token string
    raise tornado.gen.Return(access_token.access_token)
