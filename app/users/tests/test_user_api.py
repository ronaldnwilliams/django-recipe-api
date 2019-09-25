from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('users:create')
TOKEN_URL = reverse('users:token')


def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class UsersPublicAPITests(TestCase):
    """Test the users API public endpoints"""
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user when valid payload is successful"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass123',
            'name': 'Zero Sweeteners'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_user_exists(self):
        """Test creating a user that already exists fails"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass123',
            'name': 'Zero Sweeteners'
        }
        create_user(**payload)

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that the password must be more than 5 characters"""
        payload = {
            'email': 'test@test.com',
            'password': 'wef',
            'name': 'Zero Sweeteners'
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(get_user_model().objects.filter(email=payload['email']).exists())

    def test_create_token_for_user(self):
        """Test that a token is created for the user"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass123'
        }
        create_user(**payload)

        response = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that a token is not created if invalid credentials given"""
        email = 'test@test.com'
        create_user(email=email, password='testpass123')
        payload = {
            'email': email,
            'password': 'wrong password'
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not created if user does not exist"""
        payload = {
            'email': 'test@test.com',
            'password': 'testpass123'
        }

        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required for token url"""
        response_no_pw = self.client.post(TOKEN_URL, {'email': 'test@test.com', 'password': ''})
        response_no_email = self.client.post(TOKEN_URL, {'email': '', 'password': 'testpass123'})

        self.assertNotIn('token', response_no_pw)
        self.assertEqual(response_no_pw.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('token', response_no_email)
        self.assertEqual(response_no_email.status_code, status.HTTP_400_BAD_REQUEST)
