import factory
from factory.django import DjangoModelFactory
from apps.rides.models import Ride
from django.utils import timezone
from apps.users.tests.factories import RiderFactory, DriverFactory


class RideFactory(DjangoModelFactory):
    class Meta:
        model = Ride

    id_rider = factory.SubFactory(RiderFactory)
    id_driver = factory.SubFactory(DriverFactory)
    pickup_latitude = factory.Faker('latitude')
    pickup_longitude = factory.Faker('longitude')
    dropoff_latitude = factory.Faker('latitude')
    dropoff_longitude = factory.Faker('longitude')
    pickup_time = factory.LazyFunction(timezone.now)
    status = 'pickup'
    is_deleted = False

class FarRideFactory(RideFactory):
    pickup_latitude = 20.0
    pickup_longitude = 20.0
    dropoff_latitude = factory.Faker('latitude')
    dropoff_longitude = factory.Faker('longitude')
class NearRideFactory(RideFactory):
    pickup_latitude = 0.0
    pickup_longitude = 0.0
    dropoff_latitude = factory.Faker('latitude')
    dropoff_longitude = factory.Faker('longitude')