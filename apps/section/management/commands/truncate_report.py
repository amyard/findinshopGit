#-*- coding: utf-8 -*-

#Django imports
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

#Findinshop imports
from apps.cpa.models import Report


class Command(BaseCommand):
    help = 'Deleted report'

    def handle(self, *args, **kwargs):
        cursor = connection.cursor()
        cursor.execute("TRUNCATE TABLE cpa_report")

        self.stdout.write('report was deleted')
