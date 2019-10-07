#-*- coding: utf-8 -*-

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.catalog.models import Catalog, Item, ImportTask
from apps.pages.models import Page
from apps.website.models import Website


@receiver(post_save, sender=Catalog)
def create_pages(sender, created, instance, **kwargs):
    if created:
        Page.objects.bulk_create([
            Page(website=instance.website, title=u"О нас", slug="about-us", page_type=0),
            Page(website=instance.website, title=u"Как купить", slug="how-to-buy", page_type=0),
            Page(website=instance.website, title=u"Контакты", slug="contacts", page_type=0),
            Page(website=instance.website, title=u"Для партнеров", slug="for-partners", page_type=0),
            Page(website=instance.website, title=u"Дистрибуция", slug="distribution", page_type=0)
        ])


@receiver(post_save, sender=Website)
def create_catalog(sender, instance, **kwargs):
    try:
        Catalog.objects.get(website=instance)
    except Catalog.DoesNotExist:
        Catalog(website=instance).save()


@receiver(pre_save, sender=Item)
def check_category(sender, instance, **kwargs):
    try:
        if instance.category.parameters:
            for k, v in instance.category.parameters.items():
                if k not in instance.parameters.keys():
                    instance.parameters[k] = v
    except:
        pass

