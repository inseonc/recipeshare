# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipeShareApp', '0004_delete_example'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='photo',
        ),
    ]
