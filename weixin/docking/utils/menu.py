# -*-coding:utf-8 -*-
"""
Created on 11/26/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

import json

import tornado.gen

from .request import request_async
from .token import get_access_token
from exception.request import GetSelfMenuFailed
from docking.models.material import Material, NewsMessageItem, NewsMessage, NewsMessageItemsMapping, MaterialNewsMapping
from docking.models.menu import Menu
from docking.models.event import EventRule
from docking.utils.generic import generate_random_key

SELFMENU_INFO_URL = 'https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info'


@tornado.gen.coroutine
def set_menu_with_materials(account, agent, buttons, parent=0):
    for data in buttons:
        btype = data.get('type')

        menu_params = {
            'account_id': account.id,
            'account_agent_id': agent.id if agent else 0,
            'parent_id': parent,
            'name': data['name'],
        }

        if btype:
            if btype == 'view':
                menu_params.update({
                    'type': 'view',
                    'url': data['url']
                })
            elif btype in ['click', 'scancode_push', 'scancode_waitmsg', 'pic_sysphoto',
                           'pic_photo_or_album', 'pic_weixin', 'location_select']:
                menu_params.update({
                    'type': btype,
                    'key': data['key'][:16]
                })
            elif btype in ['media_id', 'view_limited']:
                menu_params.update({
                    'type': btype,
                    'media_id': data['media_id']
                })
            elif btype == 'text':
                params = {
                    'account_id': account.id,
                    'account_agent_id': agent.id if agent else 0,
                    'type': 'T',
                    'description': data['value']
                }
                material = yield Material(alias='文本消息', title='文本消息', **params).get_or_create(**params)

                key = generate_random_key()
                params = {
                    'account_id': account.id,
                    'account_agent_id': agent.id if agent else 0,
                    'key': key,
                    'material_id': material.id
                }
                yield EventRule(**params).get_or_create(**params)

                menu_params.update({
                    'type': 'click',
                    'key': key
                })
            elif btype == 'img':
                params = {
                    'account_id': account.id,
                    'account_agent_id': agent.id if agent else 0,
                    'type': 'P',
                    'media_id': data['value']
                }
                material = yield Material(alias='远程图片', **params).get_or_create(**params)

                key = generate_random_key()
                params = {
                    'account_id': account.id,
                    'account_agent_id': agent.id if agent else 0,
                    'key': key,
                    'material_id': material.id
                }
                yield EventRule(**params).get_or_create(**params)

                menu_params.update({
                    'type': 'click',
                    'key': key
                })
            elif btype == 'voice':
                params = {
                    'account_id': account.id,
                    'account_agent_id': agent.id if agent else 0,
                    'type': 'V',
                    'media_id': data['value']
                }
                material = yield Material(alias='远程语音', **params).get_or_create(**params)

                key = generate_random_key()
                params = {
                    'account_id': account.id,
                    'account_agent_id': agent.id if agent else 0,
                    'key': key,
                    'material_id': material.id
                }
                yield EventRule(**params).get_or_create(**params)

                menu_params.update({
                    'type': 'click',
                    'key': key
                })
            elif btype == 'video':
                params = {
                    'account_id': account.id,
                    'account_agent_id': agent.id if agent else 0,
                    'type': 'F',
                    'fltype': 'R',
                    'file': data['value']
                }
                material = yield Material(alias='远程视频', **params).get_or_create(**params)

                key = generate_random_key()
                params = {
                    'account_id': account.id,
                    'account_agent_id': agent.id if agent else 0,
                    'key': key,
                    'material_id': material.id
                }
                yield EventRule(**params).get_or_create(**params)

                menu_params.update({
                    'type': 'click',
                    'key': key
                })
            elif btype == 'news':
                news = yield NewsMessage(account_id=account.id,
                                         account_agent_id=agent.id if agent else 0,
                                         alias='图文消息').get_or_create()

                ordering = 1
                for item in data['news_info']['list']:
                    params = {
                        'account_id': account.id,
                        'account_agent_id': agent.id if agent else 0,
                        'title': item['title'][:16],
                        'description': item['digest'],
                        'pltype': 'R',
                        'pic_large': item['cover_url'],
                        'pic_small': item['cover_url'],
                        'url': item['content_url']
                    }
                    item = yield NewsMessageItem(**params).get_or_create()
                    yield NewsMessageItemsMapping(news_id=news.id, item_id=item.id, ordering=ordering).get_or_create(news_id=news.id, item_id=item.id)
                    ordering += 1

                params = {
                    'account_id': account.id,
                    'account_agent_id': agent.id if agent else 0,
                    'type': 'N',
                }
                material = yield Material(alias='图文消息', **params).get_or_create(**params)

                params = {
                    'material_id': material.id,
                    'news_id': news.id,
                }
                yield MaterialNewsMapping(**params).get_or_create(**params)

                key = generate_random_key()
                params = {
                    'account_id': account.id,
                    'account_agent_id': agent.id if agent else 0,
                    'key': key,
                    'material_id': material.id
                }
                yield EventRule(**params).get_or_create(**params)

                menu_params.update({
                    'type': 'click',
                    'key': key
                })
            print('menu_params:', menu_params)
            yield Menu(**menu_params).get_or_create(**menu_params)
        else:
            menu_params['type'] = 'parent'
            menu = yield Menu(**menu_params).get_or_create(**menu_params)
            yield set_menu_with_materials(account, agent, data['sub_button']['list'], parent=menu.id)


@tornado.gen.coroutine
def init_selfmenu_info(account, agent=None):
    """
    Pull the current selfmenu.
    Please note that this method will cover the current menus.

    :param account: docking.models.Account instance.
    :param agent: docking.models.Agent instance.
    :return: True if succeed.
    """

    access_token = yield get_access_token(account)

    params = {
        'access_token': access_token
    }
    response = yield request_async(SELFMENU_INFO_URL, params)

    try:
        data = json.loads(response.decode('utf8'))
    except AttributeError:
        raise GetSelfMenuFailed('Error in decoding response data.')
    except (TypeError, ValueError) as e:
        raise GetSelfMenuFailed('Error in parsing response data: {0}.'.format(e))

    # Clear existed menus.
    query = {
        'account_id': account.id
    }
    if agent:
        query['account_agent_id'] = agent.id
    yield Menu(**query).delete()

    # Parse the new menus.
    try:
        yield set_menu_with_materials(account, agent, data['selfmenu_info']['button'])
    except Exception as e:
        raise GetSelfMenuFailed('Error in parsing response data: {0}.'.format(str(e)))
