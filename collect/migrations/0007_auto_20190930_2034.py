# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-30 20:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0006_auto_20190930_1932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensor',
            name='max_value',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]