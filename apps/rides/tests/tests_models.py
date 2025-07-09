from django.test import TestCase
from apps.users.models import User, UserRoles

class CustomUserManagerTest(TestCase):
    def test_create_user_without_email_raises_error(self):
        with self.assertRaises(ValueError) as ctx:
            User.objects.create_user(email=None, password='testpass123')
        self.assertEqual(str(ctx.exception), 'Email is required')

    def test_create_user_with_valid_data(self):
        user = User.objects.create_user(
            email='juan@example.com',
            password='securepass123',
            first_name='Test',
            last_name='User',
            role=UserRoles.RIDER
        )
        self.assertEqual(user.email, 'juan@example.com')
        self.assertTrue(user.check_password('securepass123'))
        self.assertEqual(user.role, UserRoles.RIDER)
        self.assertFalse(user.is_superuser) 

    def test_create_superuser_defaults_to_admin_role(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertEqual(admin.email, 'admin@example.com')
        self.assertTrue(admin.check_password('adminpass123'))
        self.assertEqual(admin.role, UserRoles.ADMIN)