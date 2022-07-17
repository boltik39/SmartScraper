from django.db import models


class DeviceDescription(models.Model):
    query = models.TextField
    mttr = models.DecimalField
    mtbf = models.DecimalField
    failure_rate = models.DecimalField
    failure_rate_in_storage_mode = models.DecimalField
    storage_time = models.DecimalField
    minimal_resource = models.DecimalField
    gamma_percentage_resource = models.DecimalField
    average_resource = models.DecimalField
    average_lifetime = models.DecimalField
    recovery_intensity = models.DecimalField
    system_reliability = models.DecimalField
    score = models.IntegerField
