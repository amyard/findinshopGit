# -*- coding:utf-8 -*-
import os

from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.db import models
import mimetypes

from utils.enum_choices import EnumChoices
from utils.upload import get_section_path
from utils.fields import ContentTypeRestrictedFileField


class Website(models.Model):
    SKINS = EnumChoices((
        (0, u'Базовая тема', 'BASIC'),
        (1, u'Техно', 'TECHNO'),
        (2, u'Нарвик', 'NARWIK'),
        (3, u'Остерио', 'OSTERIO'),
        (4, u'Мода', 'FASHION'),
    ))

    STATE = EnumChoices((
        (0, u'Неактивен', 'INACTIVE'),
        (1, u'Активен', 'ACTIVE'),
    ))

    HAVE_YML = EnumChoices((
        (0, u'Нет', 'No'),
        (1, u'Да', 'Yes'),

    ))

    LOCATION = EnumChoices((
        (0, u'На сервере', 'No'),
        (1, u'Удаленно', 'Yes'),

    ))

    TYPE = EnumChoices((
        (0, _('Online'), 'ONLINE'),
        (1, _('Offline'), 'OFFLINE'),
    ))

    user = models.OneToOneField('auth.User', related_name='website')
    domain = models.CharField(verbose_name=u'Домен', max_length=255, blank=True, null=True)
    subdomain = models.CharField(
        verbose_name=u'Субдомен', max_length=255, unique=True, blank=True, null=True)
    name = models.CharField(max_length=255, verbose_name=u'Название')
    logo = models.ImageField(verbose_name=u'Лого', upload_to=get_section_path, blank=True, null=True)
    logo_map = models.ImageField(verbose_name=u'Значек магазина на карте', upload_to=get_section_path,
                                 blank=True, null=True, help_text=u'Удачный размер 32х32')
    skin = models.IntegerField(choices=SKINS, default=0, verbose_name=u'Оформление')
    ga_id = models.CharField(verbose_name=u'Google Analytics Tracking ID', max_length=255, blank=True, null=True)
    ym_id = models.IntegerField(verbose_name=u'Yandex Metric ID', blank=True, null=True)
    li_id = models.CharField(verbose_name=u'Live Internet', max_length=255, blank=True, null=True)
    mr_id = models.CharField(verbose_name=u'Mail@Ru', max_length=255, blank=True, null=True)
    keywords = models.CharField(verbose_name=u'Ключевые слова (SEO)', max_length=400, blank=True, null=True)
    meta = models.TextField(verbose_name=u'Meta', blank=True, null=True)
    state = models.IntegerField(choices=STATE, default=0, verbose_name=u'Состояние')
    validity = models.DateTimeField(verbose_name=u'Срок действия', blank=True, null=True)
    phone_call_center = models.CharField(verbose_name=u'Телефон Call-центра', max_length=50, blank=True, null=True)

    type = models.IntegerField(choices=TYPE, default=0, verbose_name=u'Тип магазина')
    have_yml = models.IntegerField(choices=HAVE_YML, default=0, verbose_name=u'Прайс-лист YML')
    web_property = models.ForeignKey('WebsiteProperty', verbose_name=u'Тарифный план', null=True)
    location_site = models.IntegerField(choices=LOCATION, default=0, verbose_name=u'Локализация сайта')

    class Meta:
        verbose_name = 'Вебсайт'
        verbose_name_plural = 'Вебсайты'

    def get_logo_url(self):
        if self.logo:
            return self.logo.path.replace(settings.MEDIA_ROOT + '/', settings.MEDIA_URL)
        return os.path.join(settings.STATIC_URL, 'img/website.jpg')

    def get_logo_thumb50_url(self):
        if self.logo:
            filename = self.logo.path.replace(os.path.dirname(self.logo.path) + '/', '')
            thumb_filename = filename
            thumb_path = self.logo.path.replace(filename, thumb_filename)
            return thumb_path.replace(settings.MEDIA_ROOT + '/', settings.MEDIA_URL)
        return os.path.join(settings.STATIC_URL, 'img/website.jpg')

    def get_section(self):
        return ('sitelogo')

    def __unicode__(self):
        return u'%s.%s' % (self.subdomain, settings.BASE_DOMAIN)


# @receiver(post_save, sender=User)
# def create_website(sender, instance, **kwargs):
#     try:
#         Website.objects.get(user=instance)
#     except Website.DoesNotExist:
#         Website(user=instance, subdomain=instance.username.lower()).save()
#

class UserSpaceManager(models.Manager):
    use_for_related_fields = True

    def __getattr__(self, key):
        if self.instance:
            try:
                return UserSpace.objects.get(website=self.instance, key=key)
            except UserSpace.DoesNotExist:
                UserSpace(website=self.instance, key=key, content='').save()
                return ''


class UserSpace(models.Model):
    website = models.ForeignKey(Website, verbose_name=u'Вебсайт', blank=True, null=True, related_name='spaces')
    key = models.CharField(verbose_name=u'Позиция', max_length=50, blank=True, null=True)
    content = models.TextField(verbose_name=u'Содержание', blank=True, null=True)
    banner_content = ContentTypeRestrictedFileField(
        verbose_name=u'Баннер',
        upload_to=get_section_path,
        content_types=['image/jpeg', 'image/png', 'image/gif', 'application/x-shockwave-flash'],
        max_upload_size=2621440,
        blank=True,
        null=True
    )
    banner_url = models.URLField(verbose_name=u'Ссылка', blank=True, null=True)

    objects = UserSpaceManager()

    class Meta:
        verbose_name = 'UserSpace'
        verbose_name_plural = 'UserSpaces'

    def get_section(self):
        return ('website_banner')

    def is_flash(self):
        if mimetypes.guess_type(self.banner_content.name)[0] == 'application/x-shockwave-flash':
            return True
        else:
            return False

    def __unicode__(self):
        return u'Контент для %s' % self.website


class WebsiteProperty(models.Model):
    SEL = EnumChoices((
        (0, u'Нет', 'No'),
        (1, u'Да', 'Yes'),

    ))
    name = models.CharField(verbose_name=u'Наименование', max_length=100)
    price = models.FloatField(verbose_name=u'Стоимость', blank=True, null=True)
    product_max = models.IntegerField(verbose_name=u'Максимум товара')
    validity = models.IntegerField(verbose_name=u'Срок действия(мес.)', default=0, blank=True, null=True)
    template_selection = models.IntegerField(choices=SEL, default=0, verbose_name=u'Выбор шаблона')
    domain = models.IntegerField(choices=SEL, default=0, verbose_name=u'Свой домен')
    imp_from_exel = models.IntegerField(choices=SEL, default=0, verbose_name=u'Импорт из MS Excel')
    imp_from_xml = models.IntegerField(choices=SEL, default=0, verbose_name=u'Импорт из XML')
    imp_from_xmlHP = models.IntegerField(choices=SEL, default=0, verbose_name=u'Импорт из XML(HotPrice)')
    imp_from_yml = models.IntegerField(choices=SEL, default=0, verbose_name=u'Импорт из YML')
    imp_from_1c = models.IntegerField(choices=SEL, default=0, verbose_name=u'Импорт из 1C')
    exp_from_yml = models.IntegerField(choices=SEL, default=0, verbose_name=u'Экспорт в YML')
    exp_from_xls = models.IntegerField(choices=SEL, default=0, verbose_name=u'Экспорт в MS Excel')
    google_analistics = models.IntegerField(choices=SEL, default=0, verbose_name=u'Подключение к Google Analytics')
    yandex_metrika = models.IntegerField(choices=SEL, default=0, verbose_name=u'Подключение к Yandex Metrika')
    setting_discounts = models.IntegerField(choices=SEL, default=0, verbose_name=u'Настройка скидок')
    cabinet_buyer = models.IntegerField(choices=SEL, default=0, verbose_name=u'Кабинет покупателя')
    filter_goods = models.IntegerField(choices=SEL, default=0, verbose_name=u'Фильтр по товарам')
    goods_main_site = models.IntegerField(choices=SEL, default=0, verbose_name=u'Показ товаров на основном сайте')
    help_setting_shop = models.IntegerField(choices=SEL, default=0, verbose_name=u'Помощь в настройке магазина')
    additional_functionality = models.IntegerField(choices=SEL, default=0, verbose_name=u'Дополнительный функционал')
    sales_credit_installments = models.IntegerField(choices=SEL, default=0, verbose_name=u'Продажа в расскрочку/кредит')
    exclusive_design = models.IntegerField(choices=SEL, default=0, verbose_name=u'Разработка эксклюзивного дизайна')
    integration_privatbank = models.IntegerField(choices=SEL, default=0,
                                                 verbose_name=u'Интеграция платежных систем "Приват Банк"')
    third_party_advertising = models.IntegerField(choices=SEL, default=0, verbose_name=u'Сторонняя рекламма на сайте')

    customer_reviews = models.IntegerField(choices=SEL, default=0, verbose_name=u'Отзывы клиентов')
    compare_products = models.IntegerField(choices=SEL, default=0, verbose_name=u'Сравнение товаров')
    integration_one_c = models.IntegerField(choices=SEL, default=0, verbose_name=u'Интеграция с 1C')

    news = models.IntegerField(choices=SEL, default=0, verbose_name=u'Новости')
    display_banners = models.IntegerField(choices=SEL, default=0, verbose_name=u'Отображение баннеров')
    online_shop = models.IntegerField(choices=SEL, default=0, verbose_name=u'Интернет-магазин')

    class Meta:
        verbose_name = u'Настройки вебсайтов'
        verbose_name_plural = u'Настройки вебсайтов'

    def __unicode__(self):
        return self.name


class Point(models.Model):
    STORE = 'ST'
    POINT = 'PN'
    STORE_AND_POINT = 'STPN'
    KINDS = (
        (STORE, u'Магазин'),
        (POINT, u'Пункт выдачи'),
        (STORE_AND_POINT, u'Магазин и пункт выдачи'),
    )
    outlet_id = models.CharField(max_length=100, blank=True, null=True)
    name_1c = models.CharField(u'Название в 1С',
                               max_length=255,
                               help_text=u'Название точки в 1С',
                               blank=True)
    user = models.ForeignKey(User)
    kind = models.CharField(u'Тип',
                            choices=KINDS,
                            max_length=10
                            )
    name = models.CharField(u'Название',
                            max_length=255,
                            help_text=u'Удобное для запоминания название точки'
                            )
    name_1c = models.CharField(u'Название в YML',
                               max_length=255,
                               help_text=u'Название точки в YML',
                               blank=True)
    approve = models.BooleanField(u'Одобрен', default=False, help_text=u'Будет ли отображатся магазин на сайте')
    city = models.CharField(u'Город', max_length=255, )
    street = models.CharField(u'Улица', max_length=255, )
    address = models.CharField(u'Адрес', max_length=255, )
    lat = models.CharField(u'Lat', max_length=100, blank=True, null=True)
    lon = models.CharField(u'Lon', max_length=100, blank=True, null=True)
    notes = models.TextField(u'Как добраться',
                             help_text=u'Корпус, этаж, как удобнее добраться',
                             blank=True,
                             null=True
                             )
    phone = models.CharField(u'Телефон',
                             max_length=20,
                             blank=True,
                             null=True
                             )
    weekdays_from = models.CharField(u'с',
                                     max_length=5,
                                     blank=True,
                                     null=True
                                     )
    weekdays_to = models.CharField(u'до',
                                   max_length=5,
                                   blank=True,
                                   null=True
                                   )
    saturday_from = models.CharField(u'с',
                                     max_length=5,
                                     blank=True,
                                     null=True
                                     )
    saturday_to = models.CharField(u'до',
                                   max_length=5,
                                   blank=True,
                                   null=True
                                   )
    sunday_from = models.CharField(u'с',
                                   max_length=5,
                                   blank=True,
                                   null=True
                                   )
    sunday_to = models.CharField(u'до',
                                 max_length=5,
                                 blank=True,
                                 null=True
                                 )
    terminal = models.BooleanField(u'Наличие терминала по приему платежей',
                                   default=False
                                   )
    on_map = models.BooleanField(u'Показывать на карте',
                                 default=True
                                 )

    def get_html_description(self):
        """
            Rerurn description for map
        """
        description = ''
        if self.notes:
            description += '\
                <p class="p-shop-notes">%s</p>' % self.notes
        return ' '.join(description.splitlines())

    def __unicode__(self):
        return u'%s.%s' % (self.name, self.city)
