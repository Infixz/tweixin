# -*-coding:utf-8 -*-
"""
Created on 11/26/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import unicode_literals


from core.models import SingleObjectModel
from utils.generic import get_timestamp_now


class Menu(SingleObjectModel):
    """
    The Menu Model Class for quick query.
    """

    db_table = 'docking_menu'
    fields = ['id', 'account_id', 'account_agent_id', 'parent_id', 'name', 'type', 'key', 'url', 'media_id']
    defaults = {
        'created': get_timestamp_now,
        'media_id': '',
        'url': '',
        'key': '',
        'account_agent_id': 0
    }
