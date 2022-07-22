from django.db import models


class Device(models.Model):
    name = models.CharField(max_length=255)
    mttr = models.FloatField()
    mtbf = models.FloatField()
    failure_rate = models.FloatField()
    failure_rate_in_storage_mode = models.FloatField()
    storage_time = models.FloatField()
    minimal_resource = models.FloatField()
    gamma_percentage_resource = models.FloatField()
    average_resource = models.FloatField()
    average_lifetime = models.FloatField()
    recovery_intensity = models.FloatField()
    system_reliability = models.FloatField()
    score = models.IntegerField()
    link = models.TextField()