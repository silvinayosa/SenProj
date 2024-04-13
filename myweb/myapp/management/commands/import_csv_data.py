
import csv
from django.core.management.base import BaseCommand
from myapp.models import co2

class Command(BaseCommand):
    help = 'Import CO2 data from a CSV file'

    def handle(self, *args, **kwargs):
        csv_file_path = r'C:\Users\lingh\OneDrive\桌面\Senior\myweb\datasets\CO2.csv'
        with open(csv_file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row
            for row in reader:
                time, co2_value, latitude, longitude = row
                co2.objects.create(time=time, co2=float(co2_value), latitude=float(latitude), longitude=float(longitude))
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))



