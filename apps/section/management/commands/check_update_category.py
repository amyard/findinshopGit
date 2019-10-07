#-*- coding: utf-8 -*-

#Django imports
from django.core.management.base import BaseCommand, CommandError

#Findinshop imports
from apps.catalog.models import Category
from django.db import connection, transaction


class Command(BaseCommand):
    help = 'Parser catogories from Megamax'

    def handle(self, *args, **kwargs):
        category = Category.objects.filter(parameters__isnull=True)
        print category.count()
        category.update(parameters={})

        cursor = connection.cursor()
        cursor.execute('''ALTER TABLE  
                            cpa_ownandusercategory_categories 
                        DROP CONSTRAINT  
                            category_id_refs_id_15c47a68;
                    ''')
        transaction.commit_unless_managed()

        self.stdout.write('Category is check successfully.')
