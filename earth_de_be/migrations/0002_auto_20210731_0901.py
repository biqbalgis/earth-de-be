# Generated by Django 3.2.4 on 2021-07-31 09:01

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('earth_de_be', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='downloaded_in_project',
            name='img_path',
        ),
        migrations.CreateModel(
            name='downloaded_rasters',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('raster_extent', models.CharField(blank=True, max_length=255, null=True)),
                ('raster_srid', models.CharField(blank=True, max_length=50, null=True)),
                ('image_size', models.FloatField(blank=True, null=True)),
                ('img_path', models.CharField(blank=True, max_length=500, null=True)),
                ('downloaded_dt', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('downloaded_date', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='earth_de_be.downloaded_in_project')),
            ],
        ),
    ]
