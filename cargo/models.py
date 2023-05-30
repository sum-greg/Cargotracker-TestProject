import random
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()


class Truck(models.Model):
    number_validator = RegexValidator(
        regex=r'^\d{4}[A-Z]$',
        message='Number should be in the format 4 digits followed by an uppercase letter.',
    )

    number = models.CharField(max_length=5,
                              unique=True,
                              validators=[number_validator])
    current_location = models.ForeignKey(Location, on_delete=models.CASCADE)
    capacity = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])

    def update_location(self):
        all_locations = Location.objects.exclude(id=self.current_location_id)
        random_location = random.choice(all_locations)
        self.current_location = random_location
        self.save()


class Cargo(models.Model):
    pickup_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='pickups')
    delivery_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='deliveries')
    weight = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)])
    description = models.TextField()
