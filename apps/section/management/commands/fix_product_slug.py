#-*- coding: utf-8 -*-

#Django imports
from django.core.management.base import BaseCommand, CommandError

#Findinshop imports
from apps.section.models import ProductModel


class Command(BaseCommand):
    help = 'Clean slug'

    def handle(self, *args, **kwargs):
        dirty = [' ', '/', '\'', '"', ',', '.', ')', '(', '&', '$', '*', ':', '@', '!', '~', '`', '+', '=', '?', ';', '>', '<', '[', ']', '|', u'№']
        for char in dirty:
            products = ProductModel.objects.filter(slug__icontains=char)
            print products.count(), char
            for p in products:
                p.slug = p.slug.replace(char, '')
                p.save()
