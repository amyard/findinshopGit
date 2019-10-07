# -*- coding: utf-8 -*-
from django.db import models


class News(models.Model):
    website = models.ForeignKey('website.Website', blank=True, null=True, related_name='news')
    title = models.CharField(verbose_name=u'Заголовок', max_length=255)
    text = models.TextField(verbose_name=u'Содержание')
    date = models.DateTimeField(verbose_name=u'Дата', auto_now_add=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['-date']
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
