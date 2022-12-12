from django.contrib import admin
from .models import Weather,Corn_grain_yield,DataAnalysis
# Register your models here.

admin.site.register(Weather)
admin.site.register(Corn_grain_yield)
admin.site.register(DataAnalysis)
