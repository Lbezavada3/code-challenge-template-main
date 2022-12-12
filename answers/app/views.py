from django.shortcuts import render
from rest_framework import parsers
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import FileUploadParser
from .models import Weather,Corn_grain_yield,DataAnalysis
import pandas as pd
import os
import datetime
from django.db.models import Max, Min, Avg, Sum
from django.db.models.functions import TruncMonth, TruncYear


from .serializers import WeatherDetailSerializer,Corn_grain_yieldDetailSerializer,DataAnalysisSerializer
# Create your views here.

class WeatherList(APIView):
    """
    List all campaign, or create a new campaign.    
    """
    def add_argument(self, parser):
        pass

    def format_date(self, date):
        return date[:4] + '-' + date[4:6]+'-' + date[6:]

    
    def get(self, request, format=None):
        api_response = {'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'status': 'failed', 'messages': [], 'data': []}
       
        paginator = PageNumberPagination()
        w_data = Weather.objects.all()
        context = paginator.paginate_queryset(w_data, request)
        serializer = WeatherDetailSerializer(context, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        try:

            num_of_records_before_insert = Weather.objects.all().count()
            start_time = datetime.datetime.now()

            # loop through the weather data files
            files = os.listdir('../wx_data/')
            for file in files:
                if file.endswith(".txt"):
                    # load data into pandas data frame
                    df = pd.read_csv(f"../wx_data/{str(file)}", sep="\t", header=None, names=['date', 'max_temp', 'min_temp', 'precipitation'])
                    df_records = df.to_dict('records')
                    # load data from data frame to model instances
                    model_instances = [Weather(
                        station_id=str(file.split('.')[0]),
                        date=self.format_date(str(record['date'])),
                        max_temp=record['max_temp'],
                        min_temp=record['min_temp'],
                        precipitation=record['precipitation']
                    ) for record in df_records]

                    # use django bulk_create to insert data into tables
                    Weather.objects.bulk_create(model_instances, ignore_conflicts=True)

            finish_time = datetime.datetime.now()
            num_of_records_after_insert = Weather.objects.all().count()


            data = {"messages":"data added.","start_time":start_time,"end":finish_time,"execution_time ":finish_time - start_time,"Number of records ingested":num_of_records_after_insert-num_of_records_before_insert}
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as e:
            data=[]
            data["messages"] = "Error"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
class Corn_grain_yieldList(APIView):
    """
    List all campaign, or create a new campaign.    
    """
    

    def get(self, request, format=None):
        api_response = {'status_code': status.HTTP_500_INTERNAL_SERVER_ERROR, 'status': 'failed', 'messages': [], 'data': []}
       
        paginator = PageNumberPagination()
        w_data = Corn_grain_yield.objects.all()
        context = paginator.paginate_queryset(w_data, request)
        serializer = Corn_grain_yieldDetailSerializer(context, many=True)

        return paginator.get_paginated_response(serializer.data)

    def post(self, request, format=None):
        try:
           
            num_of_records_before_insert = Corn_grain_yield.objects.all().count()
            start_time = datetime.datetime.now()
            # load data into pandas data frame
            df = pd.read_csv("../yld_data/US_corn_grain_yield.txt", sep="\t", header=None, names=['year', 'corn_yield'])
            df_records = df.to_dict('records')
            # load data from data frame to model instances
            model_instances = [Corn_grain_yield(
                year=record['year'],
                corn_yield=record['corn_yield'],
            ) for record in df_records]
            # use django bulk_create to insert data into tables
            Corn_grain_yield.objects.bulk_create(model_instances, ignore_conflicts=True)
            finish_time = datetime.datetime.now()
            num_of_records_after_insert = Corn_grain_yield.objects.all().count()
            data = {"messages":"data added.","start_time":start_time,"end":finish_time,"execution_time ":finish_time - start_time,"Number of records ingested":num_of_records_after_insert-num_of_records_before_insert}

            return Response(data, status=status.HTTP_201_CREATED)
       
        except Exception as e:
            data=[]
            data["messages"]=str(e)
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
    
class DataAnalysisList(APIView):
    def get(self, request, format=None):
        get_data = request.query_params
        if len(get_data) == 0:
            w_data = DataAnalysis.objects.all()
        else:
            kwargs = {i: get_data[i] for i in get_data}
            w_data = DataAnalysis.objects.filter(**kwargs)

        paginator = PageNumberPagination()

        context = paginator.paginate_queryset(w_data, request)
        serializer = DataAnalysisSerializer(context, many=True)

        return paginator.get_paginated_response(serializer.data)


    def post(self, request, format=None):
       
        try:
            num_of_records_before_insert = DataAnalysis.objects.all().count()
            start_time = datetime.datetime.now()
            weather_data = Weather.objects.all().count()
            if weather_data == 0:
                print("No Data available to analyze weather")
                return Response("No Data available to analyze weather", status=status.HTTP_201_CREATED)

            w_data = list(Weather.objects.exclude(max_temp=-9999,precipitation=-9999).annotate(year=TruncYear('date')).values("station_id","date__year").annotate(max_temp_avg=Avg('max_temp'),min_temp_avg=Avg('min_temp'),total_precipitation=Sum('precipitation')))

            print(len(w_data))
            products = [DataAnalysis(station_id=w_datum["station_id"], year=w_datum["date__year"], max_temp_avg=w_datum["max_temp_avg"], min_temp_avg=w_datum["min_temp_avg"], total_precipitation=w_datum["total_precipitation"]) for w_datum in w_data]

            DataAnalysis.objects.bulk_create(products,ignore_conflicts=True)

            finish_time = datetime.datetime.now()
            num_of_records_after_insert = DataAnalysis.objects.all().count()
            data = {"messages":"data added.","start_time":start_time,"end":finish_time,"execution_time ":finish_time - start_time,"Number of records ingested":num_of_records_after_insert-num_of_records_before_insert}
            return Response(data, status=status.HTTP_201_CREATED)

        except Exception as e:
            data=[]
            print(e)
            data["messages"]="error"
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
