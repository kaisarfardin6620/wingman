from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.verify_otp_url = reverse('verify-otp')
        self.user_data = {
            'email': 'test@example.com',
            'password': 'StrongPassw0rd!',
            'confirm_password': 'StrongPassw0rd!'
        }

    @patch('authentication.services.send_otp_via_email')
    def test_user_registration(self, mock_send_otp):
        mock_send_otp.return_value = (True, "OTP sent")
        response = self.client.post(self.register_url, self.user_data)
        
        if response.status_code == 400:
            print(f"Reg Error: {response.data}")
            
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')

    def test_registration_password_mismatch(self):
        data = self.user_data.copy()
        data['confirm_password'] = 'wrongpassword'
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('authentication.services.send_otp_via_email')
    def test_login_success(self, mock_send_otp):
        User.objects.create_user(email='test@example.com', password='StrongPassw0rd!', is_active=True)
        
        data = {'email': 'test@example.com', 'password': 'StrongPassw0rd!'}
        response = self.client.post(self.login_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_login_invalid_credentials(self):
        User.objects.create_user(email='test@example.com', password='StrongPassw0rd!', is_active=True)
        data = {'email': 'test@example.com', 'password': 'wrong'}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('authentication.services.verify_otp_via_email')
    def test_verify_otp(self, mock_verify):
        User.objects.create_user(email='test@example.com', password='StrongPassw0rd!', is_active=False)
        
        mock_verify.return_value = (True, "Success")
        data = {'email': 'test@example.com', 'otp': '1234'}
        response = self.client.post(self.verify_otp_url, data)
        
        if response.status_code == 400:
            print(f"OTP Error: {response.data}")
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)