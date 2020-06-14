# Generated by Django 3.0.7 on 2020-06-14 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0010_auto_20200614_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='plotfile',
            name='sensor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='plots', to='collect.Sensor'),
            preserve_default=False,
        ),
    ]
