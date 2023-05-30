import os
import csv
import django

# Конфигурация настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'testcargotracker.settings')
django.setup()

from cargo.models import Location
from django.db import transaction


@transaction.atomic
def load_data():
    with open('uszips.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            location = Location(
                city=row['city'],
                state=row['state_id'],
                zip_code=row['zip'],
                latitude=float(row['lat']),
                longitude=float(row['lng'])
            )
            location.save()


load_data()
