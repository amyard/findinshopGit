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
from apps.section.models import Measure


dse.patch_models(specific_models=[Measure])


class Command(BaseCommand):
    help = 'Parse measures from IceCat'

    def handle(self, *args, **kwargs):
        file_source = os.path.join(settings.MEDIA_ROOT, 'icecat/MeasuresList.xml')
        tree = ET.parse(file_source)

        # with transaction.commit_on_success():
        #     with Measure.delayed as m:
        for measure in tree.iter('Measure'):
            data = {}
            data['inner_id'] = int(measure.get('ID'))
            data['sign'] = u'%s' % measure.findtext('Sign')
            for name in measure.findall('./Names/Name'):
                if name.get('langid') == '8':
                    data['name'] = u'%s' % name.text
            for sign in measure.findall('./Signs/Sign'):
                if sign.get('langid') == '8':
                    data['sign_rus'] = u'%s' % sign.text
            # m.insert(data)
            m = Measure(**data)
            m.save()

        self.stdout.write('Measures have uploaded successfully.')
