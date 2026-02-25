from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from chat.models import ChatSession, Message, MessageImage
from unittest.mock import patch
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class ChatAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='chat@test.com', password='StrongPassw0rd!', is_active=True)
        self.client.force_authenticate(user=self.user)
        self.session = ChatSession.objects.create(user=self.user, title="Test Chat")
        self.list_url = reverse('chat-sessions-list')
        self.detail_url = reverse('chat-sessions-detail', args=[self.session.conversation_id])

    def test_list_chat_sessions(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if 'results' in response.data:
            self.assertEqual(len(response.data['results']), 1)
        else:
            self.assertEqual(len(response.data), 1)

    def test_rename_session(self):
        url = reverse('chat-sessions-rename', args=[self.session.conversation_id])
        data = {'title': 'Updated Title'}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.session.refresh_from_db()
        self.assertEqual(self.session.title, 'Updated Title')

    def test_delete_session(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ChatSession.objects.count(), 0)

    @patch('chat.tasks.analyze_screenshot_task.delay')
    def test_image_upload(self, mock_task):
        url = reverse('session-upload', args=[self.session.conversation_id])
        
        file_obj1 = BytesIO()
        img1 = Image.new('RGB', (100, 100), color='red')
        img1.save(file_obj1, format='JPEG')
        file_obj1.seek(0)
        
        file_obj2 = BytesIO()
        img2 = Image.new('RGB', (100, 100), color='blue')
        img2.save(file_obj2, format='JPEG')
        file_obj2.seek(0)
        
        image1 = SimpleUploadedFile("test1.jpg", file_obj1.read(), content_type="image/jpeg")
        image2 = SimpleUploadedFile("test2.jpg", file_obj2.read(), content_type="image/jpeg")
        
        response = self.client.post(url, {'images': [image1, image2]}, format='multipart')
        
        if response.status_code == 400:
            print(f"Upload Error: {response.data}")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        msg = Message.objects.filter(session=self.session).last()
        self.assertIsNotNone(msg)
        self.assertEqual(msg.images.count(), 2)
        mock_task.assert_called_once()