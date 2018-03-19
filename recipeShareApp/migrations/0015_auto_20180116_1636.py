# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipeShareApp', '0014_auto_20180116_1634'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='photo',
            field=models.ImageField(default=b'../Chrysanthemum.jpg', null=True, upload_to=b'photo/%Y/%m/%d', blank=True),
        ),
    ]
