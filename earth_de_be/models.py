from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.utils.timezone import now
from simple_history.models import HistoricalRecords

MESSAGE_TYPE_CHOICES = (
    ('error', 'error'), ('log', 'log'), ('thread_log', 'thread_log'), ('thread_error', 'thread_error'))


class ActivityLog(models.Model):
    id = models.AutoField(primary_key=True)
    message_type = models.CharField(max_length=50, choices=MESSAGE_TYPE_CHOICES)
    message = models.TextField()
    request_path = models.CharField(max_length=255, blank=True, null=True)
    stack_trace = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    log_date = models.DateTimeField(default=now)


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=200, null=True, blank=True)
    aoi = models.GeometryField()
    created_at = models.DateTimeField(null=True, blank=True, default=now)
    created_by = models.CharField(null=True, blank=True, max_length=50)


class downloaded_in_project(models.Model):
    id = models.AutoField(primary_key=True)
    downloading_date = models.DateField(null=True, blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)


class downloaded_rasters(models.Model):
    id = models.AutoField(primary_key=True)
    downloaded_date = models.ForeignKey(downloaded_in_project, on_delete=models.CASCADE)
    raster_extent = models.CharField(max_length=255, null=True, blank=True)
    raster_srid = models.CharField(max_length=50, null=True, blank=True)
    image_size = models.FloatField(null=True, blank=True)
    img_path = models.CharField(max_length=500, null=True, blank=True)
    downloaded_dt = models.DateTimeField(null=True, blank=True, default=now)
