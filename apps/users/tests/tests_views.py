from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .factories import AdminFactory
from apps.users.models import User, UserRoles

class UsersTestCase(APITestCase):
    def setUp(self):
        self.admin = AdminFactory()
        # Token for auth
        refresh = RefreshToken.for_user(self.admin)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_user_can_register(self):
        data = {
            'email': 'juanlazy@example.com',
            'password': 'StrongPass123!',
            'phone_number': '09123123123',
            'first_name': 'Juan',
            'last_name': 'Doe',
            'role':UserRoles.ADMIN,
            'is_deleted':False
        }
        self.client.credentials()
        response = self.client.post(reverse('users-list'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_authenticated_user_can_retrieve_users(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(reverse('users-detail', args=[self.admin.pk]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.admin.email)

    def test_token_login(self):
        User.objects.create_user(
            email='juan@example.com',
            password='StrongPass123!',
            first_name='Juan',
            last_name='User',
            role=UserRoles.ADMIN,
            is_deleted=False
        )
        data = {
            'email': 'juan@example.com',
            'password': 'StrongPass123!'
        }
        response = self.client.post(reverse('token_obtain_pair'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)