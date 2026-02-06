from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()

class DashboardTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email='admin@test.com', password='StrongPassw0rd!')
        self.user = User.objects.create_user(email='user@test.com', password='StrongPassw0rd!', is_active=True)
        self.analytics_url = reverse('admin-analytics')
        self.user_list_url = reverse('admin-users-list')

    def test_analytics_access_denied_for_normal_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.analytics_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_analytics_access_granted_for_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.analytics_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_users', response.data)

    def test_admin_can_list_users(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data.get('results', response.data)
        self.assertTrue(len(data) >= 2)

    def test_admin_toggle_status(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('admin-users-toggle-status', args=[self.user.id])
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)   
        response = self.client.patch(url)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)