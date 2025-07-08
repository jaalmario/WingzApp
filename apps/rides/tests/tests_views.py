from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from apps.users.models import User, UserRoles
from apps.rides.models import Ride
from apps.ride_events.models import RideEvent
from rest_framework_simplejwt.tokens import RefreshToken
from .factories import AdminFactory, RiderFactory, DriverFactory, DeletedUserFactory

class RideListTestCase(APITestCase):
    def setUp(self):
        self.admin = AdminFactory()
        self.rider = RiderFactory()
        self.driver = DriverFactory()

        # Token for auth
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        #Farther pickup (10,20)
        self.ride = Ride.objects.create(
            id_rider=self.rider,
            id_driver=self.driver,
            pickup_latitude=10.0,
            pickup_longitude=20.0,
            dropoff_latitude=10.0,
            dropoff_longitude=20.0,
            pickup_time=timezone.now(),
            status='en-route'
        )
        
        #Nearer pickup (0,0)
        self.ride2 = Ride.objects.create(
            id_rider=self.rider,
            id_driver=self.driver,
            pickup_latitude=0.0,
            pickup_longitude=0.0,
            dropoff_latitude=10.0,
            dropoff_longitude=20.0,
            pickup_time=timezone.now(),
            status='pickup'
        )

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
        self.assertEqual(len(response.data['results'][0]['todays_ride_events']), 2)
        
    def test_filter_by_status(self):
        response = self.client.get(reverse('rides-list') + '?status=en-route')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_count'], 1)

    def test_filter_by_rider_email(self):
        response = self.client.get(reverse('rides-list') + f'?id_rider__email={self.rider.email}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['total_count'], 2)

    def test_order_by_distance_valid_coords_asc(self):
        response = self.client.get(reverse('rides-list') + '?latitude=1.1&longitude=2.1&ordering=distance')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.ride2.id_ride, response.data['results'][0]['id_ride'])
        
    def test_order_by_distance_valid_coords_dsc(self):
        response = self.client.get(reverse('rides-list') + '?latitude=1.1&longitude=2.1&ordering=-distance')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.ride.id_ride, response.data['results'][0]['id_ride'])

    def test_order_by_distance_missing_coords(self):
        response = self.client.get(reverse('rides-list') + '?ordering=distance')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unauthenticated_access(self):
        self.client.credentials()
        response = self.client.get(reverse('rides-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

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
