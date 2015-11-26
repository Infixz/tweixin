# -*-coding:utf-8 -*-
"""
Created on 11/19/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import unicode_literals

import sys

from core.models import SingleObjectModel
from utils.generic import get_timestamp_now

if not sys.version_info[0] == 2:
    unicode = str


class Account(SingleObjectModel):
    """
    The Account Model Class for quick query.
    """

    db_table = 'docking_account'
    fields = ['id', 'user_id', 'uuid', 'type', 'token', 'app_id', 'secret', 'encoding_aes_key', 'is_valid']


class Agent(SingleObjectModel):
    """
    Account Agent.
    """

    db_table = 'docking_account_agent'
    fields = ['id', 'account_id', 'agent_id', 'name']


class AccessToken(SingleObjectModel):
    """
    Saved access token for all accounts.
    """

    db_table = 'docking_access_token'
    fields = ['id', 'account_id', 'account_agent_id', 'access_token', 'created', 'expired']
    defaults = {
        'account_agent_id': 0,
        'created': get_timestamp_now
    }
    order_by = ['-expired']
