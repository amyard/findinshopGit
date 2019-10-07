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
from apps.section.models import FeatureIcecat, Measure , FeatureTypeIcecat


dse.patch_models(specific_models=[FeatureIcecat])


class Command(BaseCommand):
    help = 'Parse features from IceCat'

    def handle(self, *args, **kwargs):
        file_source = os.path.join(settings.MEDIA_ROOT, 'icecat/FeaturesList.xml')
        tree = ET.parse(file_source)
        # with transaction.commit_on_success():
        #     with FeatureIcecat.delayed as f:
        for feature in tree.iter('Feature'):
            data = {}
            data['inner_id'] = int(feature.get('ID'))

            for name in feature.findall('./Names/Name'):
                if name.get('langid') == '8':
                    data['name'] = u'%s' % name.text
            if not( 'name' in data ) :
                continue
            try:
                tupe_icecat = FeatureTypeIcecat.objects.get(types=u'%s' % feature.get('Type', ''))
            except Exception:
                tupe_icecat = FeatureTypeIcecat(types=u'%s' % feature.get('Type', ''))
                tupe_icecat.save() 
            data['types'] = tupe_icecat
            # data['types'] = u'%s' % feature.get('Type', '')
            try:
                measure = Measure.objects.filter(inner_id=int(feature.find('Measure').get('ID')))[0]
                data['measure_id'] = measure.id
            except:
                pass
            # f.insert(data)
            f = FeatureIcecat(**data)
            f.save()
                    

        self.stdout.write('Features have uploaded successfully.')
