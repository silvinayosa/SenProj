from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User
from .models import co2
from .models import Venue




class UserAdmin(admin.ModelAdmin):
    list_display = ('ID', 'FirstName', 'LastName', 'Email', 'Password', 'verification_code', 'verified', 'token', 'token_expiry')


class Co2Admin(admin.ModelAdmin):
    list_display = ('ID', 'time', 'co2', 'latitude', 'longitude')

class VenueAdmin(admin.ModelAdmin):
    list_display = ('ID','Facility_Name', 'ODRSF_facility_type', 'Prov_Terr', 'Latitude', 'Longitude')

admin.site.register(User, UserAdmin)

admin.site.register(Venue, VenueAdmin)

admin.site.register(co2, Co2Admin)