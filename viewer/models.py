from django.db import models


class ObjectInfo(models.Model):
    object_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=25)
    norad_cat_id = models.IntegerField()
    object_type = models.CharField(max_length=15)
    ops_status_code = models.CharField(max_length=15, blank=True)
    owner = models.CharField(max_length=15)
    launch_date = models.DateField()
    launch_site = models.CharField(max_length=15)
    decay_date = models.CharField(max_length=15, blank=True)
    period = models.CharField(blank=True, max_length=15)
    inclination = models.CharField(blank=True, max_length=15)
    apogee = models.CharField(blank=True, max_length=15)
    perigee = models.CharField(blank=True, max_length=15)
    rcs = models.CharField(max_length=15, blank=True)
    data_status_code = models.CharField(max_length=15, blank=True)
    orbit_center = models.CharField(max_length=15)
    orbit_type = models.CharField(max_length=15)
