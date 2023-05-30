from rest_framework import serializers
from geopy.distance import geodesic
from .models import Location, Truck, Cargo


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'


class TruckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Truck
        fields = '__all__'

    def update_location(self, instance):
        instance.update_location()
        return instance


class CargoSerializer(serializers.ModelSerializer):
    distance_to_cargo = serializers.SerializerMethodField()
    truck_numbers = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = '__all__'

    def get_distance_to_cargo(self, obj):
        pickup_location = obj.pickup_location
        delivery_location = obj.delivery_location
        distance = geodesic((pickup_location.latitude, pickup_location.longitude),
                            (delivery_location.latitude, delivery_location.longitude)).miles
        return distance

    def get_truck_numbers(self, obj):
        pickup_location = obj.pickup_location
        truck_distance_mapping = {}
        trucks = Truck.objects.all()
        for truck in trucks:
            truck_location = truck.current_location
            distance = geodesic((pickup_location.latitude, pickup_location.longitude),
                                (truck_location.latitude, truck_location.longitude)).miles
            truck_distance_mapping[truck.number] = distance
        return truck_distance_mapping
