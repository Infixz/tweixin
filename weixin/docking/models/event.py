# -*-coding:utf-8 -*-
"""
Created on 11/26/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from __future__ import unicode_literals

from core.models import SingleObjectModel
from utils.generic import get_timestamp_now


class EventRule(SingleObjectModel):
    """
    The Event Rule Model Class for quick query.
    """

    db_table = 'docking_event_rule'
    fields = ['id', 'account_id', 'account_agent_id','key', 'material_id', 'created']
    defaults = {
        'created': get_timestamp_now,
        'account_agent_id': 0
    }
