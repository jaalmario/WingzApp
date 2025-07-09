from django.test import TestCase
from apps.users.api.serializers import BaseUserSerializer, SimpleUserSerializer, CustomTokenObtainPairSerializer
from .factories import RiderFactory

class BaseUserSerializerTestCase(TestCase):
    def setUp(self):
        self.user = RiderFactory()
        self.old_password_hash = self.user.password

    def test_valid_user_creation(self):
        data = {
            'email': 'juan@example.com',
            'password': 'TestJuan234!',
            'first_name': 'Test',
            'last_name': 'User',
            'phone_number': '123456789',
            'role': 'admin'
        }
        serializer = BaseUserSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertTrue(user.check_password('TestJuan234!'))
        
    def test_user_creation_missing_email(self):
        data = {'password': 'TestJuan234!'}
        serializer = BaseUserSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)

    def test_update_with_new_password_hashes_password(self):
        new_password = "NewSecurePass123!"
        serializer = BaseUserSerializer(
            instance=self.user,
            data={
                "first_name": "Updated",
                "password": new_password,
            },
            partial=True
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        updated_user = serializer.save()

        self.assertEqual(updated_user.first_name, "Updated")
        self.assertNotEqual(updated_user.password, self.old_password_hash)
        self.assertTrue(updated_user.check_password(new_password))
        