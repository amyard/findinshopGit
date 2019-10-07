#-*- coding: utf-8 -*-

#Python imports
import os
import xml.etree.cElementTree as ET
import dse
import urllib2

#Django imports
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction
from django.core.files.temp import NamedTemporaryFile
from django.core.files import File

#Findinshop imports
from apps.section.models import ProductModel, Section, FeatureGroup, FeatureIcecat, FeatureIcecatProductConnection
from utils2.transliterate import transliterate


class Command(BaseCommand):
    help = 'Update products from IceCat'

    def handle(self, *args, **options):
        file_source = os.path.join(settings.MEDIA_ROOT, 'icecat/files.index.xml')
        tree = ET.parse(file_source)

        for product_file in tree.iter('file'):
            product = ProductModel.objects.filter(inner_id=int(product_file.get('Product_ID')))
            if product:
                if str(product_file.get('On_Market')) == '1':
                    product[0].is_new = True
                    product[0].save()

        self.stdout.write('Products have updated successfully.')
