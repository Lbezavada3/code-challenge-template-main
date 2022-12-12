from statistics import mode
from django.db import models
from bulk_update_or_create import BulkUpdateOrCreateQuerySet


# Create your models here.
#----------------    Data Modeling ----------------------------------------------------
class Weather(models.Model):

    station_id = models.CharField(max_length=30)
    date = models.DateField()
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    precipitation = models.FloatField()
    created_timestamp = models.DateTimeField(auto_now_add=True, null=False)
    updated_timestamp = models.DateTimeField(auto_now=True, null=False)
    objects = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        ordering = ['station_id']
        constraints = [
            models.UniqueConstraint(fields=['station_id', 'date'],name='unique_station_day')
        ]
    

class Corn_grain_yield(models.Model):
    year = models.PositiveSmallIntegerField(unique=True)
    corn_yield = models.FloatField()
    created_timestamp = models.DateTimeField(auto_now_add=True, null=False)
    updated_timestamp = models.DateTimeField(auto_now_add=True, null=False)

    objects = BulkUpdateOrCreateQuerySet.as_manager()

    class Meta:
        ordering = ['year']

        

class DataAnalysis(models.Model):
    station_id = models.CharField(max_length=30)
    year = models.PositiveSmallIntegerField()
    max_temp_avg = models.FloatField(null=True)
    min_temp_avg = models.FloatField(null=True)
    total_precipitation = models.FloatField(null=True)

    created_timestamp = models.DateTimeField(auto_now_add=True, null=False)
    updated_timestamp = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        ordering = ['station_id', 'year']
        constraints = [
            models.UniqueConstraint(fields=['station_id', 'year'],name='unique_station_year')
        ]


