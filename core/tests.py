from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.models import UserSettings, TargetProfile, GlobalConfig

User = get_user_model()

class CoreTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@test.com', password='password123', is_active=True)
        self.client.force_authenticate(user=self.user)
        self.settings_url = reverse('user-settings')
        self.profiles_url = reverse('target-profile-list')

    def test_get_user_settings_created_automatically(self):
        response = self.client.get(self.settings_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(UserSettings.objects.filter(user=self.user).exists())

    def test_update_user_settings(self):
        data = {'language': 'es', 'goal': 'Casual Dating'}
        response = self.client.patch(self.settings_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.settings.refresh_from_db()
        self.assertEqual(self.user.settings.language, 'es')

    def test_create_target_profile(self):
        data = {
            'name': 'Crush Name',
            'details': 'Met at coffee shop'
        }
        response = self.client.post(self.profiles_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TargetProfile.objects.count(), 1)

    def test_target_profile_limit_for_free_users(self):
        GlobalConfig.objects.create(pk=1)
        for i in range(10):
            TargetProfile.objects.create(user=self.user, name=f"Target {i}")
            
        data = {'name': 'Overflow Target'}
        response = self.client.post(self.profiles_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)