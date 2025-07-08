from django.test import TestCase
from rest_framework.exceptions import ValidationError
from apps.rides.api.serializers import BaseRideSerializer
from .factories import RiderFactory, DriverFactory
from apps.rides.models import Ride
from datetime import datetime
from zoneinfo import ZoneInfo


class BaseRideSerializerTest(TestCase):
    def setUp(self):
        self.rider = RiderFactory()
        self.driver = DriverFactory()

    def test_valid_data_passes_validation(self):
        data = {
            "id_rider": self.rider.id_user,
            "id_driver": self.driver.id_user,
            "pickup_latitude": 10.0,
            "pickup_longitude": 20.0,
            "dropoff_latitude": 11.0,
            "dropoff_longitude": 21.0,
            "pickup_time": datetime.now(tz=ZoneInfo("UTC")),
            "status": "pickup",
        }

        serializer = BaseRideSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_soft_deleted_rider_raises_validation_error(self):
        self.rider.is_deleted = True
        self.rider.save()

        data = {
            "id_rider": self.rider.id_user,
            "id_driver": self.driver.id_user,
            "pickup_latitude": 10.0,
            "pickup_longitude": 20.0,
            "dropoff_latitude": 11.0,
            "dropoff_longitude": 21.0,
            "pickup_time": datetime.now(tz=ZoneInfo("UTC")),
            "status": "pickup",
        }

        serializer = BaseRideSerializer(data=data)
        with self.assertRaises(ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)

        self.assertIn("Rider account is deactivated.", str(ctx.exception))

    def test_soft_deleted_driver_raises_validation_error(self):
        self.driver.is_deleted = True
        self.driver.save()

        data = {
            "id_rider": self.rider.id_user,
            "id_driver": self.driver.id_user,
            "pickup_latitude": 10.0,
            "pickup_longitude": 20.0,
            "dropoff_latitude": 11.0,
            "dropoff_longitude": 21.0,
            "pickup_time": datetime.now(tz=ZoneInfo("UTC")),
            "status": "pickup",
        }

        serializer = BaseRideSerializer(data=data)
        with self.assertRaises(ValidationError) as ctx:
            serializer.is_valid(raise_exception=True)

        self.assertIn("Driver account is deactivated.", str(ctx.exception))