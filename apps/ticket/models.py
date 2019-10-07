# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from utils.enum_choices import EnumChoices


class Ticket(models.Model):
    STATUS_CODES = EnumChoices((
        (0, u'Открыта', 'OPEN'),
        (1, u'Обрабатывается', 'WORKING'),
        (2, u'Закрыта', 'CLOSED'),
    ))
    PRIORITY_CODES = EnumChoices((
        (0, u'Низкий', 'LOW'),
        (1, u'Средний', 'MEDIUM'),
        (2, u'Высокий', 'HIGH'),
    ))
    title = models.CharField(verbose_name=u'Тема', max_length=100)
    submitted_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    submitter = models.ForeignKey(User, verbose_name=u'Отправитель', related_name="submitter")
    assigned_to = models.ForeignKey(User, verbose_name=u'Назначено', blank=True, null=True, related_name="assigned")
    description = models.TextField(verbose_name=u'Содержание', blank=True, null=True)
    status = models.IntegerField(verbose_name=u'Статус', default=0, choices=STATUS_CODES)
    priority = models.IntegerField(verbose_name=u'Приоритет', default=0, choices=PRIORITY_CODES)

    class Meta:
        ordering = ('status', 'priority', 'submitted_date', 'title')

    def __unicode__(self):
        return self.title

    def get_status_key(self):
        return self.STATUS_CODES.get_name(self.status)
