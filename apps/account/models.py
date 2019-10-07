#-*- coding: utf-8 -*-
import os
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from utils.enum_choices import EnumChoices
from utils.thumb import square_thumb, fit_width
from utils.upload import get_section_path


class Profile(models.Model):

    user = models.ForeignKey(User)
    email = models.EmailField(('email address'), unique=True)

    userpic = models.ImageField(verbose_name=u'Логотип', upload_to=get_section_path, blank=True, null=True)
    firmname = models.CharField(verbose_name='Название фирмы', max_length=50, blank=True, null=True)
    phone_number = models.CharField(verbose_name=u'Номер телефона', max_length=50, blank=True, null=True)
    address = models.TextField(verbose_name=u'Адрес', blank=True, null=True)
    balance = models.FloatField(u'Счет', default=0)
    clearing_account = models.CharField(verbose_name=u'Расчетный счет', max_length=50, blank=True, null=True)
    bank = models.CharField(verbose_name=u'Банк', max_length=50, blank=True, null=True)
    mfo = models.CharField(verbose_name=u'МФО', max_length=50, blank=True, null=True)
    okpo = models.CharField(verbose_name=u'ОКПО', max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    @property
    def content_type(self):
        return ContentType.objects.get_for_model(self.__class__)

    def __unicode__(self):
        return self.user.username

    def get_userpic_url(self):
        if self.userpic:
            return self.userpic.path.replace(settings.MEDIA_ROOT + '/', settings.MEDIA_URL)
        return os.path.join(settings.STATIC_URL, 'img/userpic.jpg')

    def get_userpic_thumb50_url(self):
        if self.userpic:
            filename = self.userpic.path.replace(os.path.dirname(self.userpic.path) + '/', '')
            thumb_filename = filename.replace('.', '_50.')
            thumb_path = self.userpic.path.replace(filename, thumb_filename)
            return thumb_path.replace(settings.MEDIA_ROOT + '/', settings.MEDIA_URL)
        return os.path.join(settings.STATIC_URL, 'img/userpic.jpg')

    def presence(self):
        # if cache.get(settings.PRESENCE_KEY % self.user.id):
        #     return True
        # else:
        #     return False
        return False

    def get_section(self):
        return ('userpic')

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        if self.userpic:
            fit_width(self.userpic.path, 257)
            square_thumb(self.userpic.path, 50)


class ExtendedProfile(models.Model):
    SEL = EnumChoices((
        (0, u'Нет', 'No'),
        (1, u'Да', 'Yes'),
    ))
    user = models.ForeignKey(
        User, related_name='eprofile')
    store_name = models.CharField(
        verbose_name=u'Название магазина', max_length=50, blank=True, null=True)
    link_XML = models.CharField(
        verbose_name=u'Ссылка на XML файл', max_length=255, blank=True, null=True)
    credit_sale = models.BooleanField(
        verbose_name=u'Продажа в кредит',default=False)
    payment_methods = models.CharField(
        verbose_name=u'Способы оплаты', max_length=255)
    nds = models.BooleanField(verbose_name=u'НДС', default=False)
    wholesale_trade = models.BooleanField(verbose_name=u'Оптовая продажа',default=False)
    delivery = models.CharField(verbose_name=u'Доставка', max_length=255)
    store_address = models.CharField(
        verbose_name=u'Адрес магазина', max_length=100, blank=True, null=True)

    def __unicode__(self):
        return self.user.username


# @receiver(post_save, sender=User)
# def create_profile(sender, instance, **kwargs):
#     try:
#         Profile.objects.get(user=instance)
#     except Profile.DoesNotExist:
#         Profile(user=instance).save()
#         ExtendedProfile(user=instance).save()

class SocialAccount(models.Model):
    SOCIAL_NETWORK = EnumChoices((
        (0, 'ВКонтакте', 'VKONTAKTE'),
    ))

    user = models.ForeignKey(User, related_name='social_accounts')
    social_network = models.IntegerField(choices=SOCIAL_NETWORK, default=0)
    internal_user_id = models.CharField(max_length=200)
    access_token = models.CharField(max_length=255, default='')
    access_token_expire = models.DateField(blank=True, null=True)
