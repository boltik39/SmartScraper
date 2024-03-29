# Generated by Django 4.0.5 on 2022-07-22 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mttr', models.FloatField()),
                ('mtbf', models.FloatField()),
                ('failure_rate', models.FloatField()),
                ('failure_rate_in_storage_mode', models.FloatField()),
                ('storage_time', models.FloatField()),
                ('minimal_resource', models.FloatField()),
                ('gamma_percentage_resource', models.FloatField()),
                ('average_resource', models.FloatField()),
                ('average_lifetime', models.FloatField()),
                ('recovery_intensity', models.FloatField()),
                ('system_reliability', models.FloatField()),
                ('score', models.IntegerField()),
                ('link', models.TextField()),
            ],
        ),
    ]
