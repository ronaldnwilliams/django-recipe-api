from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'testemail@email.com'
        password = 'testpass123'

        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = 'test@EMAIL.COM'

        user = get_user_model().objects.create_user(email, 'testpass123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'testpass123')
            get_user_model().objects.create_user('', 'testpass123')

    def test_create_new_super_user(self):
        """Test create new super user"""
        user = get_user_model().objects.create_super_user(
            'test123@email.com',
            'testpass123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
