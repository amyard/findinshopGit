# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import utils.upload


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtendedProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('store_name', models.CharField(max_length=50, null=True, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430', blank=True)),
                ('link_XML', models.CharField(max_length=255, null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430 \u043d\u0430 XML \u0444\u0430\u0439\u043b', blank=True)),
                ('credit_sale', models.BooleanField(default=False, verbose_name='\u041f\u0440\u043e\u0434\u0430\u0436\u0430 \u0432 \u043a\u0440\u0435\u0434\u0438\u0442')),
                ('payment_methods', models.CharField(max_length=255, verbose_name='\u0421\u043f\u043e\u0441\u043e\u0431\u044b \u043e\u043f\u043b\u0430\u0442\u044b')),
                ('nds', models.BooleanField(default=False, verbose_name='\u041d\u0414\u0421')),
                ('wholesale_trade', models.BooleanField(default=False, verbose_name='\u041e\u043f\u0442\u043e\u0432\u0430\u044f \u043f\u0440\u043e\u0434\u0430\u0436\u0430')),
                ('delivery', models.CharField(max_length=255, verbose_name='\u0414\u043e\u0441\u0442\u0430\u0432\u043a\u0430')),
                ('store_address', models.CharField(max_length=100, null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430', blank=True)),
                ('user', models.ForeignKey(related_name='eprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name=b'email address')),
                ('userpic', models.ImageField(upload_to=utils.upload.get_section_path, null=True, verbose_name='\u041b\u043e\u0433\u043e\u0442\u0438\u043f', blank=True)),
                ('firmname', models.CharField(max_length=50, null=True, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x84\xd0\xb8\xd1\x80\xd0\xbc\xd1\x8b', blank=True)),
                ('phone_number', models.CharField(max_length=50, null=True, verbose_name='\u041d\u043e\u043c\u0435\u0440 \u0442\u0435\u043b\u0435\u0444\u043e\u043d\u0430', blank=True)),
                ('address', models.TextField(null=True, verbose_name='\u0410\u0434\u0440\u0435\u0441', blank=True)),
                ('balance', models.FloatField(default=0, verbose_name='\u0421\u0447\u0435\u0442')),
                ('clearing_account', models.CharField(max_length=50, null=True, verbose_name='\u0420\u0430\u0441\u0447\u0435\u0442\u043d\u044b\u0439 \u0441\u0447\u0435\u0442', blank=True)),
                ('bank', models.CharField(max_length=50, null=True, verbose_name='\u0411\u0430\u043d\u043a', blank=True)),
                ('mfo', models.CharField(max_length=50, null=True, verbose_name='\u041c\u0424\u041e', blank=True)),
                ('okpo', models.CharField(max_length=50, null=True, verbose_name='\u041e\u041a\u041f\u041e', blank=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u041f\u0440\u043e\u0444\u0438\u043b\u044c',
                'verbose_name_plural': '\u041f\u0440\u043e\u0444\u0438\u043b\u0438',
            },
        ),
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('social_network', models.IntegerField(default=0, choices=[(0, b'\xd0\x92\xd0\x9a\xd0\xbe\xd0\xbd\xd1\x82\xd0\xb0\xd0\xba\xd1\x82\xd0\xb5')])),
                ('internal_user_id', models.CharField(max_length=200)),
                ('access_token', models.CharField(default=b'', max_length=255)),
                ('access_token_expire', models.DateField(null=True, blank=True)),
                ('user', models.ForeignKey(related_name='social_accounts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
