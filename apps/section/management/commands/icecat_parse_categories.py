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
from apps.section.models import Section
from utils2.transliterate import transliterate


dse.patch_models(specific_models=[FeatureIcecat])


class Command(BaseCommand):
    help = 'Parse features group from IceCat'

    def handle(self, *args, **kwargs):
        file_source = os.path.join(settings.MEDIA_ROOT, 'icecat/CategoriesList.xml')
        tree = ET.parse(file_source)

        #with transaction.commit_on_success():
        #    with Section.delayed as s:
        for section in tree.iter('Category'):
            data = {}
            data['inner_id'] = int(section.get('ID'))
            for name in section.findall('Name'):
                if name.get('langid') == '8':
                    data['name'] = u'%s' % name.get('Value')
            #icon
            try:
                if section.get('LowPic', None):
                    f = NamedTemporaryFile(delete=True,  dir=".")
                    f.write(urllib2.urlopen(section.get('LowPic')).read())
                    f.flush()
                    icon = File(f)
            except:
                pass

            #thumb
            try:
                if section.get('ThumbPic', None):
                    f = NamedTemporaryFile(delete=True, dir=".")
                    f.write(urllib2.urlopen(section.get('ThumbPic')).read())
                    f.flush()
                    thumb = File(f)
            except:
                pass

            if 'name' in data:
                slug = transliterate(data['name']).replace(' ', '-').replace('/', '-')
                data['slug'] = u'%s-%s' % (slug, data['inner_id'])
                s = Section(**data)
                s.icon = icon
                s.thumb = thumb
                s.save()
        #parse parents
        for section in tree.iter('Category'):
            if not section.find('ParentCategory').get('ID') == '1':
                parent = Section.objects.filter(inner_id=section.find('ParentCategory').get('ID'))
                Section.objects.filter(inner_id=int(section.get('ID'))).update(parent=parent)

                #s.insert(data)

        self.stdout.write('Features group have uploaded successfully.')
