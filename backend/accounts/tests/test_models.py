from django.test import TestCase
from accounts.models import User

class UserModelTests(TestCase):

    def test_create_user_with_email_and_name(self):
        user = User.objects.create_user(
            email='user@example.com',
            name='Test User',
            password='testpass123'
        )
        self.assertEqual(user.email, 'user@example.com')
        self.assertEqual(user.name, 'Test User')
        self.assertTrue(user.check_password('testpass123'))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        admin = User.objects.create_superuser(
            email='admin@example.com',
            name='Admin User',
            password='adminpass123'
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_email_is_required(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email='', name='No Email', password='pass')

    def test_string_representation(self):
        user = User.objects.create_user(
            email='strtest@example.com',
            name='StrTest',
            password='testpass'
        )
        self.assertEqual(str(user), 'strtest@example.com')
