# -*-coding:utf-8 -*-
"""
Created on 11/26/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

import time
import random

allowed_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


def generate_random_key():
    return str(int(time.time())) + ''.join(random.sample(allowed_string * 3, 6))
