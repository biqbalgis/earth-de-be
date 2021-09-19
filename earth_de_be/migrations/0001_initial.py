# Generated by Django 3.2.4 on 2021-07-31 08:32

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('project_name', models.CharField(blank=True, max_length=200, null=True)),
                ('aoi', django.contrib.gis.db.models.fields.GeometryField(srid=4326)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('created_by', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='downloaded_in_project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('downloading_date', models.DateField(blank=True, null=True)),
                ('img_path', models.CharField(blank=True, max_length=500, null=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='earth_de_be.project')),
            ],
        ),
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message_type', models.CharField(choices=[('error', 'error'), ('log', 'log'), ('thread_log', 'thread_log'), ('thread_error', 'thread_error')], max_length=50)),
                ('message', models.TextField()),
                ('request_path', models.CharField(blank=True, max_length=255, null=True)),
                ('stack_trace', models.TextField(blank=True, null=True)),
                ('log_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]