# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-29 01:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mingpian', '0005_auto_20160228_2009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mingpian',
            name='name',
            field=models.CharField(db_index=True, max_length=64, null=True),
        ),
    ]
