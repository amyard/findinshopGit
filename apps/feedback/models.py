#-*- coding:utf-8 -*-

from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=250, verbose_name=u'Имя')
    email = models.EmailField(verbose_name=u'Email')
    text = models.TextField(verbose_name=u'Сообщение')
    date = models.DateTimeField(auto_now=True, verbose_name=u'Дата')

    def __unicode__(self):
        return self.name
