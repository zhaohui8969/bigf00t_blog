# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-26 18:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20161126_1821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postmodel',
            old_name='categorie',
            new_name='category',
        ),
    ]
