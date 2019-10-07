# -*- coding: utf-8 -*-

#Django imports
from django.db import models


class Banner(models.Model):
    name = models.CharField(u'Название', max_length=255)
    url = models.URLField(u'Ссылка', blank=True, null=True)
    image = models.ImageField(u'Картинка', upload_to='banners')
    active = models.BooleanField(u'Показывать?', default=True)
    sort = models.SmallIntegerField(u'Приоритет в сортировке', default=0)

    def __unicode__(self):
        return u'%s' % self.name

    class Meta:
        ordering = ['-sort']
        verbose_name = u'Баннер'
        verbose_name_plural = u'Баннера'
