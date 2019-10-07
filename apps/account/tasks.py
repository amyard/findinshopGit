# coding: utf-8
from __future__ import absolute_import

from celery import task

from utils2.email import message_send

@task(ignore_result=True)
def manager_notify_task(subject, to_email, template, context=None, 
                        from_addr=None):
    message_send(subject, to_email, template, context, from_addr)
