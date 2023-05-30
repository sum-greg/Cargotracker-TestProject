from django.contrib import admin

from .models import Location, Truck, Cargo


admin.site.register(Location)
admin.site.register(Truck)
admin.site.register(Cargo)
