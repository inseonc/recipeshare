# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipeShareApp', '0016_auto_20180118_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='photo',
            field=models.ImageField(default=b'brewvieDefault.jpg', null=True, upload_to=b'photo/%Y/%m/%d', blank=True),
        ),
    ]
