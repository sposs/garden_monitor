# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-30 19:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0005_relay'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensor',
            name='max_value',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='sensor',
            name='min_value',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sensor',
            name='state',
            field=models.CharField(choices=[(b'on', b'On'), (b'off', b'Off')], default=b'off', max_length=4),
        ),
    ]
