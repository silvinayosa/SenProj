from django.db import models

# Create your models here.

class User(models.Model):
    ID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=20)
    LastName = models.CharField(max_length=20)
    Email = models.EmailField(max_length=50)
    Password = models.CharField(max_length=255)
    verification_code = models.IntegerField()
    verified = models.BooleanField(default=False)
    token = models.CharField(max_length=255)
    token_expiry = models.DateTimeField()

    def __str__(self):
        return f'{self.FirstName} {self.LastName}'

class co2(models.Model):
    ID = models.AutoField(primary_key=True)
    time = models.CharField(max_length=20)
    co2 = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f'{self.time}'

class Venue(models.Model):
    ID = models.AutoField(primary_key=True)
    Facility_Name = models.CharField(max_length=83)
    ODRSF_facility_type = models.CharField(max_length=16)
    Prov_Terr = models.CharField(max_length=7)
    Latitude = models.DecimalField(max_digits=10, decimal_places=8)
    Longitude = models.DecimalField(max_digits=11, decimal_places=8)

    def __str__(self):
        return self.Facility_Name

