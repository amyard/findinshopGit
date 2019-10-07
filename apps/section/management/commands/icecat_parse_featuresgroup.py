#-*- coding: utf-8 -*-

#Python imports
import os
import xml.etree.cElementTree as ET
import dse

#Django imports
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import transaction

#Findinshop imports
from apps.section.models import FeatureGroup


dse.patch_models(specific_models=[FeatureGroup])


class Command(BaseCommand):
    help = 'Parse features group from IceCat'

    def handle(self, *args, **kwargs):
        file_source = os.path.join(settings.MEDIA_ROOT, 'icecat/FeatureGroupsList.xml')
        tree = ET.parse(file_source)

        # with transaction.commit_on_success():
        #     with FeatureGroup.delayed as g:
        for group in tree.iter('FeatureGroup'):
            data = {}
            data['name'] = ''
            data['inner_id'] = int(group.get('ID'))
            for name in group.findall('Name'):
                if name.get('langid') == '8':
                    data['name'] = u'%s' % name.get('Value')
            # g.insert(data)
            g = FeatureGroup(**data)
            g.save()

        self.stdout.write('Features group have uploaded successfully.')
