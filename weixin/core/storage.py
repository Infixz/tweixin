# -*-coding:utf-8 -*-
"""
Created on 11/24/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

import os
import uuid
import datetime
import settings

from .file import File


class Storage(object):
    """
    A base storage class.
    """

    def path(self, name):
        return os.path.abspath(os.path.join(settings.media_root, name))

    def open(self, name, mode='rb'):
        """
        Retrieves the specified file from storage.
        """

        return File(open(self.path(name), mode))

    def save(self, name, content):
        """
        Saves new content to the file. Name will be automatically specified.
        """

        dt = datetime.datetime.now()
        path = os.path.normpath(dt.strftime('%Y/%m/%d'))

        abs_path = self.path(path)
        if not os.path.exists(abs_path):
            os.makedirs(abs_path)

        path = os.path.join(path, str(uuid.uuid4()) + os.path.splitext(name)[1])

        with open(self.path(path), 'wb') as fd:
            fd.write(content)

        return path


storage = Storage()
