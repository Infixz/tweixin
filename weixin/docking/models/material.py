# -*-coding:utf-8 -*-
"""
Created on 11/26/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import unicode_literals


from core.models import SingleObjectModel
from utils.generic import get_timestamp_now


class Material(SingleObjectModel):
    """
    The Material Model Class for quick query.

    fltype: 素材文件位置类型：
        L - 本地
        R - 远程
    file：素材文件路径：当为本地素材时，这里是本地相对路径，否则为一个 URL
    type: 素材类型
        T - 文本
        P - 图片
        M - 音乐
        V - 语音
        F - 视频
        N - 图文
    """

    db_table = 'docking_material'
    fields = ['id', 'account_id', 'account_agent_id', 'type', 'alias', 'title',
              'description', 'media_id', 'extra', 'fltype', 'file', 'created']
    defaults = {
        'created': get_timestamp_now,
        'file': '',
        'extra': '',
        'media_id': '',
        'description': '',
        'title': '',
        'fltype': 'L',
        'account_agent_id': 0
    }


class NewsMessage(SingleObjectModel):
    """
    The News Message Model Class for quick query.
    """

    db_table = 'docking_material_news'
    fields = ['id', 'account_id', 'account_agent_id', 'alias', 'created']
    defaults = {
        'created': get_timestamp_now,
        'account_agent_id': 0
    }


class NewsMessageItem(SingleObjectModel):
    """
    The News Message Item Model Class for quick query.
    """

    db_table = 'docking_material_news_item'
    fields = ['id', 'account_id', 'account_agent_id', 'title',
              'description', 'pltype', 'pic_large', 'pic_small', 'url', 'created']
    defaults = {
        'created': get_timestamp_now,
        'account_agent_id': 0,
        'pltype': 'L',
        'pic_small': '',
        'pic_large': '',
        'description': ''
    }


class MaterialNewsMapping(SingleObjectModel):
    """
    M2M query for fetching news of one material.
    """

    db_table = 'docking_material_news_mapping'
    fields = ['id', 'material_id', 'news_id']


class NewsMessageItemsMapping(SingleObjectModel):
    """
    M2M query for fetching news items of one news message.
    """

    db_table = 'docking_material_news_item_mapping'
    fields = ['id', 'news_id', 'item_id', 'ordering']
    order_by = ['ordering']
