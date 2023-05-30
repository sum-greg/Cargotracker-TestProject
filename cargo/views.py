import threading
import time
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, F
from django.db.models.expressions import Func, Value
from .models import Location, Truck, Cargo
from .serializers import LocationSerializer, TruckSerializer, CargoSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class TruckViewSet(viewsets.ModelViewSet):
    queryset = Truck.objects.all()
    serializer_class = TruckSerializer

    @action(detail=True, methods=['post'])
    def update_location(self, request, pk=None):
        truck = self.get_object()
        serializer = self.get_serializer(truck, data=request.data, partial=True)
        serializer.update_location(truck)
        return Response(serializer.data)


class CargoViewSet(viewsets.ModelViewSet):
    queryset = Cargo.objects.all()
    serializer_class = CargoSerializer

    @action(detail=True, methods=['get'])
    def cargo_info(self, request, pk=None):
        cargo = self.get_object()
        serializer = self.get_serializer(cargo)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()

        # Фильтрация по весу
        weight = self.request.query_params.get('weight')
        if weight:
            queryset = queryset.filter(weight=int(weight))

        # Фильтрация по расстоянию
        distance = self.request.query_params.get('distance')
        if distance:
            user = self.request.user
            if not user.is_anonymous and hasattr(user, 'location'):
                lat = user.location.latitude
                lon = user.location.longitude

                pickup_queryset = Location.objects.filter(truck__isnull=False)
                pickup_queryset = pickup_queryset.annotate(distance_to_cargo=Func(
                    F('point'), Value(f'POINT({lon} {lat})'),
                    function='distance',
                ))

                delivery_queryset = Location.objects.filter(truck__isnull=False)
                delivery_queryset = delivery_queryset.annotate(distance_to_cargo=Func(
                    F('point'), Value(f'POINT({lon} {lat})'),
                    function='distance',
                ))

                queryset = queryset.filter(
                    Q(pickup_location__in=pickup_queryset.filter(distance_to_cargo__lte=Distance(mi=distance))) |
                    Q(delivery_location__in=delivery_queryset.filter(distance_to_cargo__lte=Distance(mi=distance)))
                )
            else:
                # Обработка случая, когда пользователь анонимный или не имеет локации
                queryset = queryset.none()

        return queryset


def update_truck_locations():
    while True:
        trucks = Truck.objects.all()
        for truck in trucks:
            truck.update_location()
        time.sleep(180)


# Запустить задачу в отдельном потоке
thread = threading.Thread(target=update_truck_locations)
thread.daemon = True
thread.start()
