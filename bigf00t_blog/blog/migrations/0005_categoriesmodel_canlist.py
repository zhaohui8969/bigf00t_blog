# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-26 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20161126_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='categoriesmodel',
            name='canlist',
            field=models.BooleanField(default=True),
        ),
    ]