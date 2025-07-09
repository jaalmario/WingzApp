from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from apps.ride_events.models import RideEvent
from rest_framework_simplejwt.tokens import RefreshToken
from .factories import FarRideFactory, NearRideFactory
from apps.users.tests.factories import AdminFactory, RiderFactory, DriverFactory, DeletedUserFactory
from apps.rides.exceptions import CoordinatesNotFound

class RideListTestCase(APITestCase):
    def setUp(self):
        self.admin = AdminFactory()
        self.rider = RiderFactory()
        self.driver = DriverFactory()

        # Token for auth
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        #Farther pickup (10,20)
        self.ride = FarRideFactory()
        #Nearer pickup (0,0)
        self.nearRide = NearRideFactory(id_rider=self.rider, status='en-route')

        # RideEvent within 24h
        RideEvent.objects.create(
            id_ride=self.ride,
            description='some description',
            created_at=timezone.now() - timedelta(hours=1)
        )

        # RideEvent outside 24h
        RideEvent.objects.create(
            id_ride=self.ride,
            description='expired',
            created_at=timezone.now() - timedelta(days=2)
        )

    def test_list_rides_success(self):
        response = self.client.get(reverse('rides-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_count'], 2)
        self.assertIn('todays_ride_events', response.data['results'][0])
        self.assertEqual(len(response.data['results'][1]['todays_ride_events']), 2)

    def test_order_by_distance_missing_coords(self):
        self.client.get(reverse('rides-list') + '?ordering=distance')
        self.assertRaises(CoordinatesNotFound)
        
    def test_order_by_distance_asc(self):
        response = self.client.get(reverse('rides-list') + '?ordering=distance&latitude=0.0&longitude=0.0')
        self.assertEqual(response.data['results'][0]['id_ride'], self.nearRide.id_ride)
        
    def test_order_by_distance_dsc(self):
        response = self.client.get(reverse('rides-list') + '?ordering=-distance&latitude=0.0&longitude=0.0')
        self.assertEqual(response.data['results'][0]['id_ride'], self.ride.id_ride)

class RideCreateTestCase(APITestCase):
    def setUp(self):
        self.admin = AdminFactory()
        self.driver = DriverFactory()
        self.rider = RiderFactory()

        # Token for auth
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_with_invalid_status(self):
        deleted = DeletedUserFactory()
        data = {
            "id_rider": deleted.id_user,
            "id_driver": self.driver.id_user,
            "pickup_latitude": 0.0,
            "pickup_longitude": 0.0,
            "dropoff_latitude": 10.0,
            "dropoff_longitude": 20.0,
            "pickup_time": timezone.now().isoformat(),
            "status": "not-valid-status"
        }
        response = self.client.post(reverse('rides-list'),data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
