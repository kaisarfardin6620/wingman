from django.test import TestCase, override_settings
from django.contrib.auth import get_user_model
from chat.models import ChatSession, Message
from chat.tasks import generate_ai_response, generate_chat_title
import time

User = get_user_model()

@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class ChatIntegrationTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email='real_ai@test.com', password='StrongPassw0rd!', is_active=True)
        self.session = ChatSession.objects.create(user=self.user, title="New Chat")

    def test_full_ai_response_flow(self):
        print("\n>>> CONTACTING OPENAI API (Real Call)...")
        
        user_message_text = "What are 3 date ideas for a rainy day?"
        Message.objects.create(session=self.session, sender=self.user, text=user_message_text, is_ai=False)
        
        try:
            generate_ai_response.delay(self.session.id, user_message_text)
        except Exception as e:
            self.fail(f"Celery task failed (Check API Key?): {e}")

        ai_message = Message.objects.filter(session=self.session, is_ai=True).last()
        
        self.assertIsNotNone(ai_message, "AI did not create a message response")
        self.assertTrue(len(ai_message.text) > 10, "AI response was suspiciously short")
        self.assertTrue(ai_message.tokens_used > 0, "Token usage was not tracked")
        
        print(f"    AI Responded: {ai_message.text[:50]}...")

    def test_title_generation(self):
        print("\n>>> GENERATING TITLE (Real Call)...")
        
        text = "I need advice on how to text a girl I met at the gym."
        
        try:
            generate_chat_title.delay(self.session.id, text)
        except Exception as e:
             self.fail(f"Celery task failed: {e}")
            
        self.session.refresh_from_db()
        
        print(f"    Generated Title: {self.session.title}")
        
        self.assertNotEqual(self.session.title, "New Chat")
        self.assertTrue(len(self.session.title) > 0)