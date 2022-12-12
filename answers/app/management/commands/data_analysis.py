from django.core.management.base import BaseCommand

from app.models import Weather,DataAnalysis
from django.db.models import Max, Min, Avg, Sum
import datetime
from django.db.models.functions import TruncMonth, TruncYear


class Command(BaseCommand):
    help = 'Analyze aand insert/update Weather Statistics Data'

    def add_argument(self, parser):
        pass

    def format_date(self, date):
        return f'{date[:4]}-{date[4:6]}-{date[6:]}'

    def handle(self, *args, **options):
        num_of_records_before_insert = DataAnalysis.objects.all().count()
        start_time = datetime.datetime.now()
        weather_data = Weather.objects.all().count()
        if weather_data == 0:
            print("No data available to analyze weather")

        w_data = list(Weather.objects.exclude(max_temp=-9999,precipitation=-9999).annotate(year=TruncYear('date')).values("station_id","date__year").annotate(max_temp_avg=Avg('max_temp'),min_temp_avg=Avg('min_temp'),total_precipitation=Sum('precipitation')))

        print(len(w_data))
        products = [DataAnalysis(station_id=w_datum["station_id"], year=w_datum["date__year"], max_temp_avg=w_datum["max_temp_avg"], min_temp_avg=w_datum["min_temp_avg"], total_precipitation=w_datum["total_precipitation"]) for w_datum in w_data]

        DataAnalysis.objects.bulk_create(products,ignore_conflicts=True)

        finish_time = datetime.datetime.now()
        num_of_records_after_insert = DataAnalysis.objects.all().count()

        # using print as log statement for test purposes
        print("Weather statistics data \n")
        print(f"Start Time {start_time}" + "\n")
        print(f"Finish Time {finish_time}" + "\n")
        print(f"Number of records ingested: {num_of_records_after_insert - num_of_records_before_insert}" + "\n")
        print(f"Execution time =  {finish_time - start_time} \n")
        

