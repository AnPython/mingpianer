# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mingpian', '0002_mingpian_validity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mingpian',
            name='openid',
            field=models.CharField(max_length=128, null=True, unique=True),
        ),
    ]
