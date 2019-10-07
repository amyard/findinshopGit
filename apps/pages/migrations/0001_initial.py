# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='\u041d\u0430\u0437\u0432\u0430\u043d\u0438\u0435')),
                ('text', models.TextField(verbose_name='\u0421\u043e\u0434\u0435\u0440\u0436\u0430\u043d\u0438\u0435')),
                ('slug', models.SlugField()),
                ('visibility', models.BooleanField(default=True, help_text=b'\xd0\x9f\xd0\xbe\xd1\x81\xd1\x82\xd0\xb0\xd0\xb2\xd1\x8c\xd1\x82\xd0\xb5 \xd1\x8d\xd1\x82\xd1\x83 \xd0\xbe\xd1\x82\xd0\xbc\xd0\xb5\xd1\x82\xd0\xba\xd1\x83 \xd0\xb5\xd1\x81\xd0\xbb\xd0\xb8 \xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x86\xd0\xb0 \xd1\x83\xd0\xb6\xd0\xb5 \xd0\xb7\xd0\xb0\xd0\xba\xd0\xbe\xd0\xbd\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb0 \xd0\xb8 \xd0\xb3\xd0\xbe\xd1\x82\xd0\xbe\xd0\xb2\xd0\xb0 \xd0\xba \xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xb0\xd1\x86\xd0\xb8\xd0\xb8', verbose_name=b'\xd0\x9e\xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb0')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='\u0414\u0430\u0442\u0430')),
                ('page_type', models.IntegerField(default=1, choices=[(0, '\u0412\u0441\u0442\u0440\u043e\u0435\u043d\u043d\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430'), (1, '\u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c\u0441\u043a\u0430\u044f \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u0430')])),
                ('position', models.IntegerField(default=1, verbose_name='\u0420\u0430\u0441\u043f\u043e\u043b\u043e\u0436\u0435\u043d\u0438\u0435', choices=[(0, '\u041e\u0442\u0441\u0443\u0442\u0441\u0442\u0432\u0443\u0435\u0442'), (1, '\u0428\u0430\u043f\u043a\u0430 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b'), (2, '\u041e\u0441\u043d\u043e\u0432\u0430\u043d\u0438\u0435 \u0441\u0442\u0440\u0430\u043d\u0438\u0446\u044b')])),
                ('website', models.ForeignKey(related_name='pages', blank=True, to='website.Website', null=True)),
            ],
            options={
                'ordering': ['page_type', '-title'],
                'verbose_name': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430',
                'verbose_name_plural': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b',
            },
        ),
        migrations.AlterUniqueTogether(
            name='page',
            unique_together=set([('website', 'slug')]),
        ),
    ]
