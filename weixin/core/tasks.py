# -*-coding:utf-8 -*-
"""
Created on 11/24/2015

@author: Danny<manyunkai@hotmail.com>
DannyWork Project.
"""

from celery import Celery, platforms


celery = Celery('tasks', broker='amqp://danny:111@192.168.141.130')
celery.conf.CELERY_RESULT_BACKEND = 'amqp'

platforms.C_FORCE_ROOT = True


@celery.task(name='core.tasks.write_file_simple')
def write_file_simple(fp, content):
    with open(fp, 'wb') as f:
        f.write(content)

    return True


if __name__ == "__main__":
    celery.start()
