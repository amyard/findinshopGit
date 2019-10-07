# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import utils.upload
from django.conf import settings
import utils.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Point',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('outlet_id', models.CharField(max_length=100, null=True, blank=True)),
                ('kind', models.CharField(max_length=10, verbose_name='\u0422\u0438\u043f', choices=[(b'ST', '\u041c\u0430\u0433\u0430\u0437\u0438\u043d'), (b'PN', '\u041f\u0443\u043d\u043a\u0442 \u0432\u044b\u0434\u0430\u0447\u0438'), (b'STPN', '\u041c\u0430\u0433\u0430\u0437\u0438\u043d \u0438 \u043f\u0443\u043d\u043a\u0442 \u0432\u044b\u0434\u0430\u0447\u0438')])),
                ('name', models.CharField(help_text='\u0423\u0434\u043e\u0431\u043d\u043e\u0435 \u0434\u043b\u044f \u0437\u0430\u043f\u043e\u043c\u0438\u043d\u0430\u043d\u0438\u044f \u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0442\u043e\u0447\u043a\u0438', max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('name_1c', models.CharField(help_text='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0442\u043e\u0447\u043a\u0438 \u0432 YML', max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0432 YML', blank=True)),
                ('approve', models.BooleanField(default=False, help_text='\u0411\u0443\u0434\u0435\u0442 \u043b\u0438 \u043e\u0442\u043e\u0431\u0440\u0430\u0436\u0430\u0442\u0441\u044f \u043c\u0430\u0433\u0430\u0437\u0438\u043d \u043d\u0430 \u0441\u0430\u0439\u0442\u0435', verbose_name='\u041e\u0434\u043e\u0431\u0440\u0435\u043d')),
                ('city', models.CharField(max_length=255, verbose_name='\u0413\u043e\u0440\u043e\u0434')),
                ('street', models.CharField(max_length=255, verbose_name='\u0423\u043b\u0438\u0446\u0430')),
                ('address', models.CharField(max_length=255, verbose_name='\u0410\u0434\u0440\u0435\u0441')),
                ('lat', models.CharField(max_length=100, null=True, verbose_name='Lat', blank=True)),
                ('lon', models.CharField(max_length=100, null=True, verbose_name='Lon', blank=True)),
                ('notes', models.TextField(help_text='\u041a\u043e\u0440\u043f\u0443\u0441, \u044d\u0442\u0430\u0436, \u043a\u0430\u043a \u0443\u0434\u043e\u0431\u043d\u0435\u0435 \u0434\u043e\u0431\u0440\u0430\u0442\u044c\u0441\u044f', null=True, verbose_name='\u041a\u0430\u043a \u0434\u043e\u0431\u0440\u0430\u0442\u044c\u0441\u044f', blank=True)),
                ('phone', models.CharField(max_length=20, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d', blank=True)),
                ('weekdays_from', models.CharField(max_length=5, null=True, verbose_name='\u0441', blank=True)),
                ('weekdays_to', models.CharField(max_length=5, null=True, verbose_name='\u0434\u043e', blank=True)),
                ('saturday_from', models.CharField(max_length=5, null=True, verbose_name='\u0441', blank=True)),
                ('saturday_to', models.CharField(max_length=5, null=True, verbose_name='\u0434\u043e', blank=True)),
                ('sunday_from', models.CharField(max_length=5, null=True, verbose_name='\u0441', blank=True)),
                ('sunday_to', models.CharField(max_length=5, null=True, verbose_name='\u0434\u043e', blank=True)),
                ('terminal', models.BooleanField(default=False, verbose_name='\u041d\u0430\u043b\u0438\u0447\u0438\u0435 \u0442\u0435\u0440\u043c\u0438\u043d\u0430\u043b\u0430 \u043f\u043e \u043f\u0440\u0438\u0435\u043c\u0443 \u043f\u043b\u0430\u0442\u0435\u0436\u0435\u0439')),
                ('on_map', models.BooleanField(default=True, verbose_name='\u041f\u043e\u043a\u0430\u0437\u044b\u0432\u0430\u0442\u044c \u043d\u0430 \u043a\u0430\u0440\u0442\u0435')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSpace',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=50, null=True, verbose_name='\u041f\u043e\u0437\u0438\u0446\u0438\u044f', blank=True)),
                ('content', models.TextField(null=True, verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435', blank=True)),
                ('banner_content', utils.fields.ContentTypeRestrictedFileField(upload_to=utils.upload.get_section_path, null=True, verbose_name='\u0411\u0430\u043d\u043d\u0435\u0440', blank=True)),
                ('banner_url', models.URLField(null=True, verbose_name='\u0421\u0441\u044b\u043b\u043a\u0430', blank=True)),
            ],
            options={
                'verbose_name': 'UserSpace',
                'verbose_name_plural': 'UserSpaces',
            },
        ),
        migrations.CreateModel(
            name='Website',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('domain', models.CharField(max_length=255, null=True, verbose_name='\u0414\u043e\u043c\u0435\u043d', blank=True)),
                ('subdomain', models.CharField(max_length=255, unique=True, null=True, verbose_name='\u0421\u0443\u0431\u0434\u043e\u043c\u0435\u043d', blank=True)),
                ('name', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('logo', models.ImageField(upload_to=utils.upload.get_section_path, null=True, verbose_name='\u041b\u043e\u0433\u043e', blank=True)),
                ('logo_map', models.ImageField(help_text='\u0423\u0434\u0430\u0447\u043d\u044b\u0439 \u0440\u0430\u0437\u043c\u0435\u0440 32\u044532', upload_to=utils.upload.get_section_path, null=True, verbose_name='\u0417\u043d\u0430\u0447\u0435\u043a \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430 \u043d\u0430 \u043a\u0430\u0440\u0442\u0435', blank=True)),
                ('skin', models.IntegerField(default=0, verbose_name='\u041e\u0444\u043e\u0440\u043c\u043b\u0435\u043d\u0438\u0435', choices=[(0, '\u0411\u0430\u0437\u043e\u0432\u0430\u044f \u0442\u0435\u043c\u0430'), (1, '\u0422\u0435\u0445\u043d\u043e'), (2, '\u041d\u0430\u0440\u0432\u0438\u043a'), (3, '\u041e\u0441\u0442\u0435\u0440\u0438\u043e'), (4, '\u041c\u043e\u0434\u0430')])),
                ('ga_id', models.CharField(max_length=255, null=True, verbose_name='Google Analytics Tracking ID', blank=True)),
                ('ym_id', models.IntegerField(null=True, verbose_name='Yandex Metric ID', blank=True)),
                ('li_id', models.CharField(max_length=255, null=True, verbose_name='Live Internet', blank=True)),
                ('mr_id', models.CharField(max_length=255, null=True, verbose_name='Mail@Ru', blank=True)),
                ('keywords', models.CharField(max_length=400, null=True, verbose_name='\u041a\u043b\u044e\u0447\u0435\u0432\u044b\u0435 \u0441\u043b\u043e\u0432\u0430 (SEO)', blank=True)),
                ('meta', models.TextField(null=True, verbose_name='Meta', blank=True)),
                ('state', models.IntegerField(default=0, verbose_name='\u0421\u043e\u0441\u0442\u043e\u044f\u043d\u0438\u0435', choices=[(0, '\u041d\u0435\u0430\u043a\u0442\u0438\u0432\u0435\u043d'), (1, '\u0410\u043a\u0442\u0438\u0432\u0435\u043d')])),
                ('validity', models.DateTimeField(null=True, verbose_name='\u0421\u0440\u043e\u043a \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f', blank=True)),
                ('phone_call_center', models.CharField(max_length=50, null=True, verbose_name='\u0422\u0435\u043b\u0435\u0444\u043e\u043d Call-\u0446\u0435\u043d\u0442\u0440\u0430', blank=True)),
                ('type', models.IntegerField(default=0, verbose_name='\u0422\u0438\u043f \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430', choices=[(0, 'Online'), (1, 'Offline')])),
                ('have_yml', models.IntegerField(default=0, verbose_name='\u041f\u0440\u0430\u0439\u0441-\u043b\u0438\u0441\u0442 YML', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('location_site', models.IntegerField(default=0, verbose_name='\u041b\u043e\u043a\u0430\u043b\u0438\u0437\u0430\u0446\u0438\u044f \u0441\u0430\u0439\u0442\u0430', choices=[(0, '\u041d\u0430 \u0441\u0435\u0440\u0432\u0435\u0440\u0435'), (1, '\u0423\u0434\u0430\u043b\u0435\u043d\u043d\u043e')])),
                ('user', models.OneToOneField(related_name='website', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u0412\u0435\u0431\u0441\u0430\u0439\u0442',
                'verbose_name_plural': '\u0412\u0435\u0431\u0441\u0430\u0439\u0442\u044b',
            },
        ),
        migrations.CreateModel(
            name='WebsiteProperty',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='\u041d\u0430\u0438\u043c\u0435\u043d\u043e\u0432\u0430\u043d\u0438\u0435')),
                ('price', models.FloatField(null=True, verbose_name='\u0421\u0442\u043e\u0438\u043c\u043e\u0441\u0442\u044c', blank=True)),
                ('product_max', models.IntegerField(verbose_name='\u041c\u0430\u043a\u0441\u0438\u043c\u0443\u043c \u0442\u043e\u0432\u0430\u0440\u0430')),
                ('validity', models.IntegerField(default=0, null=True, verbose_name='\u0421\u0440\u043e\u043a \u0434\u0435\u0439\u0441\u0442\u0432\u0438\u044f(\u043c\u0435\u0441.)', blank=True)),
                ('template_selection', models.IntegerField(default=0, verbose_name='\u0412\u044b\u0431\u043e\u0440 \u0448\u0430\u0431\u043b\u043e\u043d\u0430', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('domain', models.IntegerField(default=0, verbose_name='\u0421\u0432\u043e\u0439 \u0434\u043e\u043c\u0435\u043d', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('imp_from_exel', models.IntegerField(default=0, verbose_name='\u0418\u043c\u043f\u043e\u0440\u0442 \u0438\u0437 MS Excel', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('imp_from_xml', models.IntegerField(default=0, verbose_name='\u0418\u043c\u043f\u043e\u0440\u0442 \u0438\u0437 XML', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('imp_from_xmlHP', models.IntegerField(default=0, verbose_name='\u0418\u043c\u043f\u043e\u0440\u0442 \u0438\u0437 XML(HotPrice)', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('imp_from_yml', models.IntegerField(default=0, verbose_name='\u0418\u043c\u043f\u043e\u0440\u0442 \u0438\u0437 YML', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('imp_from_1c', models.IntegerField(default=0, verbose_name='\u0418\u043c\u043f\u043e\u0440\u0442 \u0438\u0437 1C', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('exp_from_yml', models.IntegerField(default=0, verbose_name='\u042d\u043a\u0441\u043f\u043e\u0440\u0442 \u0432 YML', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('exp_from_xls', models.IntegerField(default=0, verbose_name='\u042d\u043a\u0441\u043f\u043e\u0440\u0442 \u0432 MS Excel', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('google_analistics', models.IntegerField(default=0, verbose_name='\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435 \u043a Google Analytics', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('yandex_metrika', models.IntegerField(default=0, verbose_name='\u041f\u043e\u0434\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u0435 \u043a Yandex Metrika', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('setting_discounts', models.IntegerField(default=0, verbose_name='\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0430 \u0441\u043a\u0438\u0434\u043e\u043a', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('cabinet_buyer', models.IntegerField(default=0, verbose_name='\u041a\u0430\u0431\u0438\u043d\u0435\u0442 \u043f\u043e\u043a\u0443\u043f\u0430\u0442\u0435\u043b\u044f', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('filter_goods', models.IntegerField(default=0, verbose_name='\u0424\u0438\u043b\u044c\u0442\u0440 \u043f\u043e \u0442\u043e\u0432\u0430\u0440\u0430\u043c', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('goods_main_site', models.IntegerField(default=0, verbose_name='\u041f\u043e\u043a\u0430\u0437 \u0442\u043e\u0432\u0430\u0440\u043e\u0432 \u043d\u0430 \u043e\u0441\u043d\u043e\u0432\u043d\u043e\u043c \u0441\u0430\u0439\u0442\u0435', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('help_setting_shop', models.IntegerField(default=0, verbose_name='\u041f\u043e\u043c\u043e\u0449\u044c \u0432 \u043d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0435 \u043c\u0430\u0433\u0430\u0437\u0438\u043d\u0430', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('additional_functionality', models.IntegerField(default=0, verbose_name='\u0414\u043e\u043f\u043e\u043b\u043d\u0438\u0442\u0435\u043b\u044c\u043d\u044b\u0439 \u0444\u0443\u043d\u043a\u0446\u0438\u043e\u043d\u0430\u043b', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('sales_credit_installments', models.IntegerField(default=0, verbose_name='\u041f\u0440\u043e\u0434\u0430\u0436\u0430 \u0432 \u0440\u0430\u0441\u0441\u043a\u0440\u043e\u0447\u043a\u0443/\u043a\u0440\u0435\u0434\u0438\u0442', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('exclusive_design', models.IntegerField(default=0, verbose_name='\u0420\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430 \u044d\u043a\u0441\u043a\u043b\u044e\u0437\u0438\u0432\u043d\u043e\u0433\u043e \u0434\u0438\u0437\u0430\u0439\u043d\u0430', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('integration_privatbank', models.IntegerField(default=0, verbose_name='\u0418\u043d\u0442\u0435\u0433\u0440\u0430\u0446\u0438\u044f \u043f\u043b\u0430\u0442\u0435\u0436\u043d\u044b\u0445 \u0441\u0438\u0441\u0442\u0435\u043c "\u041f\u0440\u0438\u0432\u0430\u0442 \u0411\u0430\u043d\u043a"', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('third_party_advertising', models.IntegerField(default=0, verbose_name='\u0421\u0442\u043e\u0440\u043e\u043d\u043d\u044f\u044f \u0440\u0435\u043a\u043b\u0430\u043c\u043c\u0430 \u043d\u0430 \u0441\u0430\u0439\u0442\u0435', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('customer_reviews', models.IntegerField(default=0, verbose_name='\u041e\u0442\u0437\u044b\u0432\u044b \u043a\u043b\u0438\u0435\u043d\u0442\u043e\u0432', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('compare_products', models.IntegerField(default=0, verbose_name='\u0421\u0440\u0430\u0432\u043d\u0435\u043d\u0438\u0435 \u0442\u043e\u0432\u0430\u0440\u043e\u0432', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('integration_one_c', models.IntegerField(default=0, verbose_name='\u0418\u043d\u0442\u0435\u0433\u0440\u0430\u0446\u0438\u044f \u0441 1C', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('news', models.IntegerField(default=0, verbose_name='\u041d\u043e\u0432\u043e\u0441\u0442\u0438', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('display_banners', models.IntegerField(default=0, verbose_name='\u041e\u0442\u043e\u0431\u0440\u0430\u0436\u0435\u043d\u0438\u0435 \u0431\u0430\u043d\u043d\u0435\u0440\u043e\u0432', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
                ('online_shop', models.IntegerField(default=0, verbose_name='\u0418\u043d\u0442\u0435\u0440\u043d\u0435\u0442-\u043c\u0430\u0433\u0430\u0437\u0438\u043d', choices=[(0, '\u041d\u0435\u0442'), (1, '\u0414\u0430')])),
            ],
            options={
                'verbose_name': '\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0432\u0435\u0431\u0441\u0430\u0439\u0442\u043e\u0432',
                'verbose_name_plural': '\u041d\u0430\u0441\u0442\u0440\u043e\u0439\u043a\u0438 \u0432\u0435\u0431\u0441\u0430\u0439\u0442\u043e\u0432',
            },
        ),
        migrations.AddField(
            model_name='website',
            name='web_property',
            field=models.ForeignKey(verbose_name='\u0422\u0430\u0440\u0438\u0444\u043d\u044b\u0439 \u043f\u043b\u0430\u043d', to='website.WebsiteProperty', null=True),
        ),
        migrations.AddField(
            model_name='userspace',
            name='website',
            field=models.ForeignKey(related_name='spaces', verbose_name='\u0412\u0435\u0431\u0441\u0430\u0439\u0442', blank=True, to='website.Website', null=True),
        ),
    ]
