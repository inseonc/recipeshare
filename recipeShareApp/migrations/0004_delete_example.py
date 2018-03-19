# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipeShareApp', '0003_example'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Example',
        ),
    ]
