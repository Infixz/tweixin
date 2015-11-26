# -*-coding:utf-8 -*-
"""
Created on 11/19/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import unicode_literals

from core.models import SingleObjectModel
from utils.generic import get_timestamp_now


class WXUser(SingleObjectModel):
    """
    The User Model Class for quick query.
    """

    db_table = 'docking_user'
    fields = ['id', 'account_id', 'account_agent_id', 'openid', 'created', 'is_active', 'is_canceled']
    defaults = {
        'created': get_timestamp_now,
        'account_agent_id': 0,
        'is_active': 1,
        'is_canceled': 0
    }
