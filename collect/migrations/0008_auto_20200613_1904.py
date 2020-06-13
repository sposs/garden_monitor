# Generated by Django 3.1a1 on 2020-06-13 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0007_auto_20190930_2034'),
    ]

    operations = [
        migrations.CreateModel(
            name='Encoder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('rpi_port', models.IntegerField(default=2)),
                ('steps', models.IntegerField(default=32)),
                ('refresh_interval', models.IntegerField(default=5, help_text='In seconds')),
            ],
        ),
        migrations.AddField(
            model_name='sensor',
            name='power_relay',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='probes', to='collect.relay'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='sensor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='measures', to='collect.sensor'),
        ),
        migrations.AlterField(
            model_name='relay',
            name='rpi_type',
            field=models.CharField(choices=[('analog', 'Analog'), ('digital', 'Digital')], default='digital', max_length=100),
        ),
        migrations.AlterField(
            model_name='relay',
            name='state',
            field=models.CharField(choices=[('on', 'On'), ('off', 'Off')], default='off', max_length=4),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='rpi_type',
            field=models.CharField(choices=[('analog', 'Analog'), ('digital', 'Digital')], default='analog', max_length=100),
        ),
        migrations.AlterField(
            model_name='sensor',
            name='state',
            field=models.CharField(choices=[('on', 'On'), ('off', 'Off')], default='off', max_length=4),
        ),
        migrations.CreateModel(
            name='EncoderMeasurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('value', models.IntegerField(null=True)),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='measures', to='collect.encoder')),
            ],
            options={
                'ordering': ('-date',),
                'get_latest_by': 'date',
            },
        ),
        migrations.CreateModel(
            name='EncoderLimit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('min_value', models.IntegerField()),
                ('max_value', models.IntegerField()),
                ('sensor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='limits', to='collect.encoder')),
            ],
        ),
    ]