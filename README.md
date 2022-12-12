# Code Challenge Template

## Project Setup
- Python Version: python>=3.9
- Create and activate a virtual environment - using Makefile or manual
  -  `make venv`
  or Manual
  - `python3 -m venv <env>`
  - `source <env>/bin/activate`
- Apply Database Migrations
  - `python manage.py makemigrations`
  - `python manage.py migrate`
  - `python manage.py makemigrations app`
  - `python manage.py migrate app`

## Data Ingestion
- Ingesting crop and weather data using following commands
  - `python manage.py weather_data`
  - `python manage.py yield_data`

## Data Analysis
- Weather Stats are computed for pair of station_id and year possible using following command:
  - `python manage.py data_analysis`

## REST APIs
- Django REST Framework was used to develop the following 3 REST API GET endpoints with default 
    pagination 50 records and filter arguments per assignment:
  - /api/weather 
  - /api/yield
  - /api/weather/stats


- Ingesting crop and weather data using following commands    [Note: user POST method]
  - /api/weather 
  - /api/yield
  - /api/weather/stats

  Examples below and refer api postman screenshots in Answers folder for the following GET api responses:
  
  `http://localhost:8000/api/yield/`
  `http://localhost:8000/api/weather/?page=3`
  `http://localhost:8000/api/weather/stats?page=10`
  `http://localhost:8000/api/weather/stats?page=1&year=1985`
    
    
