from django.test import TestCase
from apps.rides.models import Ride
from apps.rides.services import annotate_rides_with_distance
from math import isclose
from .factories import FarRideFactory
from apps.users.tests.factories import AdminFactory, RiderFactory, DriverFactory

class AnnotateRidesWithDistanceTest(TestCase):
    def setUp(self):
        self.admin = AdminFactory()
        self.rider = RiderFactory()
        self.driver = DriverFactory()

        self.ride = FarRideFactory()

    def test_distance_annotation_present(self):
        annotated_qs = annotate_rides_with_distance(Ride.objects.all(), latitude=10.0, longitude=20.0)
        ride = annotated_qs.first()
        self.assertTrue(hasattr(ride, 'distance'))
        self.assertIsInstance(ride.distance, float)

    def test_distance_is_zero_when_same_location(self):
        annotated_qs = annotate_rides_with_distance(Ride.objects.filter(pk=self.ride.pk), latitude=20.0, longitude=20.0)
        ride = annotated_qs.first()
        self.assertTrue(isclose(ride.distance, 0.0, abs_tol=0.001))

    def test_invalid_coordinates_raise(self):
        with self.assertRaises(ValueError):
            annotate_rides_with_distance(Ride.objects.all(), latitude="invalid", longitude="invalid")