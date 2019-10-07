#-*- coding: utf-8 -*-

#Django imports
from django.core.management.base import BaseCommand, CommandError

#Findinshop imports
from apps.section.models import Section


class Command(BaseCommand):
    help = 'Deleted all sectios'

    def handle(self, *args, **kwargs):
        Section.objects.all().update(deleted=True)

        self.stdout.write('All categories were deleted.')
