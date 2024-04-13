import csv
from django.core.management.base import BaseCommand
from myapp.models import Venue

class Command(BaseCommand):
    help = 'Import venue data from a CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = r'C:\Users\lingh\OneDrive\桌面\Senior\myweb\datasets\Venue.csv'
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                facility_name, facility_type, prov_terr, latitude, longitude = row
                Venue.objects.create(
                    Facility_Name=facility_name,
                    ODRSF_facility_type=facility_type,
                    Prov_Terr=prov_terr,
                    Latitude=float(latitude),
                    Longitude=float(longitude)
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
