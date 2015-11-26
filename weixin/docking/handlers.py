# -*-coding:utf-8 -*-
"""
Created on 11/17/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import unicode_literals

import time
import hashlib
import base64
from bs4 import BeautifulSoup

import tornado.web
import tornado.gen

from .utils.cryptor import Prpcrypt, WXBizMsgCrypt
from exception.db import ObjectNotExists
from docking.models.config import Account
from docking.models.user import WXUser


class Entry(tornado.web.RequestHandler):
    """
    Entry for Wechat server access.
    """

    # Just for test.
    # ACCOUNT_TYPE = 'M'
    # APP_ID = 'wx098d830462ffddf2'
    # APP_SECRET = 'b61bc732cde486cf6edba0dbafe09a9c'
    # ENCODING_AES_KEY = 'fSRvkJF9vST3PQP6HNPwUSFSYnAtdnPMpVGSWInCbOg'
    # TOKEN = 'e0tfkOrPyfwhFR82QgdxIap8YEVih3YB'

    account = None
    user = None
    rev_xml = None

    def get_soup(self, encrypt_type, msg_signature, timestamp, nonce, body):
        if encrypt_type == 'aes':
            decrypt = WXBizMsgCrypt(self.account.token, self.account.encoding_aes_key, self.account.app_id)
            ret, content = decrypt.decrypt_msg(body, msg_signature, timestamp, nonce)
        else:
            content = body
        return BeautifulSoup(content or '', features='xml')

    def validate(self):
        signature = self.get_argument('signature' if self.account.type == 'M' else 'msg_signature', '')
        timestamp = self.get_argument('timestamp', '')
        nonce = self.get_argument('nonce',  '')
        echo_str = self.get_argument('echostr', '')

        l = [self.account.token, timestamp, nonce]
        if self.account.type == 'Q':
            if echo_str:
                l.append(echo_str)
            else:
                if not self.rev_xml or not self.rev_xml.Encrypt:
                    return False
                l.append(self.rev_xml.Encrypt.text)
        l.sort()

        tmp_str = hashlib.sha1(''.join(l).encode('utf8')).hexdigest()
        if tmp_str == signature:
            return True

        return False

    @tornado.gen.coroutine
    def prepare(self):
        # Check associated account.
        uuid = self.path_args[0]
        try:
            self.account = yield Account(uuid=uuid).get()
        except ObjectNotExists:
            raise tornado.web.HTTPError(403)

        # Validate request.
        if not self.validate():
            raise tornado.web.HTTPError(403)

    @tornado.gen.coroutine
    def get_user(self, openid):
        query = {
            'account_id': self.account.id,
            'openid': openid,
        }
        user = yield WXUser(**query).get_or_create(is_canceled=0, **query)
        raise tornado.gen.Return(user)

    def encrypt_res(self, content):
        encrypt = WXBizMsgCrypt(self.account.token, self.account.encoding_aes_key, self.account.app_id)
        ret, content = encrypt.encrypt_msg(content,
                                           self.get_argument('nonce', ''),
                                           self.get_argument('timestamp', ''))
        return content

    def get(self, uuid, *args, **kwargs):
        if not self.validate():
            raise tornado.web.HTTPError(403)

        echo_str = self.get_argument('echostr', '')
        if self.account.type == 'Q':
            # 企业号需解密 echostr
            key = base64.b64decode(self.account.encoding_aes_key + '=')
            if not len(key) == 32:
                # 无效的 encoding_aes_key
                raise tornado.web.HTTPError(403)

            pc = Prpcrypt(key)
            ret, echo_str = pc.decrypt(echo_str, self.account.app_id)
            if ret:
                # 解密错误
                raise tornado.web.HTTPError(403)
        self.write(echo_str)

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        # Parse received XML.
        encrypt_type = self.get_argument('encrypt_type', 'raw') if self.account.type == 'M' else 'aes'

        # 企业号始终为 AES 加密模式
        # 公众号根据 encrypt_type 参数判断
        soup = self.get_soup(encrypt_type,
                             self.get_argument('msg_signature', ''),
                             self.get_argument('timestamp', ''),
                             self.get_argument('nonce', ''),
                             self.request.body.decode('utf8'))

        user = yield self.get_user(soup.FromUserName.text)

        # TODO ...
        params = {
            'to_user': user.openid,
            'from_user': soup.ToUserName.text,
            'msg_type': 'text',
            'create_time': int(time.time()),
            'reply': {
                'content': 'HELLO!'
            }
        }
        content = self.render_string('message_reply.xml', autoescape=None, **params)
        content = self.encrypt_res(content) if content and encrypt_type == 'aes' else content
        self.write(content)
