# -*- coding: utf-8 -*-
from django.db import models
# from django.core.urlresolvers import reverse
from utils.enum_choices import EnumChoices


class VersionManager(models.Manager):
    use_for_related_fields = True

    def __getattr__(self, key):
        """
        тут нужно сделать так чтобы получать доступ к включенным версиям
        что-то типа этого request.user.versions.WEBSITE должен вернуть True или False
        в зависимоти от того есть ли запись в бд или нет
        """
        if self.instance:
            version_type = self.model.TYPE._enums.get(key)
            if isinstance(version_type, int):
                try:
                    self.get(type=version_type, user=self.instance)
                    return True
                except self.model.DoesNotExist:
                    return False
                raise AttributeError
        else:
            raise AttributeError


class Version(models.Model):
    """
    Модель для когтроля доступа юзера к кам-то фичам системы
    так как мы будем продавать какието фичи за денги в будущем
    Все доступные ключи должны быть оперделены в переменной TYPE
    """
    TYPE = EnumChoices((
        (0, u'Покупка в рассрочку', 'INSTALLMENT'),
        (1, u'Обратная связь', 'FEEDBACK'),
    ))
    user = models.ForeignKey('auth.User', related_name='versions')
    type = models.IntegerField(choices=TYPE)
    date = models.DateTimeField(verbose_name=u'Дата', auto_now_add=True)

    objects = VersionManager()

    def __unicode__(self):
        return u'%s: %s' % (self.user, self.type)

    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        unique_together = ('user', 'type')
