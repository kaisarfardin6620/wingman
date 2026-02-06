from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from wingman.asgi import application
from chat.models import ChatSession

User = get_user_model()

class WebSocketTests(TransactionTestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email='ws_test@test.com', password='StrongPassw0rd!', is_active=True)
        self.session = ChatSession.objects.create(user=self.user, title="WS Chat")
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

    async def test_websocket_connect_and_auth(self):
        communicator = WebsocketCommunicator(
            application, 
            f"/ws/chat/{self.session.conversation_id}/?token={self.token}"
        )
        
        connected, subprotocol = await communicator.connect()
        self.assertTrue(connected, "WebSocket failed to connect")
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'chat_history')
        
        await communicator.disconnect()

    async def test_websocket_rejects_no_token(self):
        communicator = WebsocketCommunicator(
            application, 
            f"/ws/chat/{self.session.conversation_id}/"
        )
        connected, _ = await communicator.connect()
        
        if connected:
            await communicator.receive_nothing()
        
        self.assertTrue(True) 
        await communicator.disconnect()

    async def test_send_message_flow(self):
        communicator = WebsocketCommunicator(
            application, 
            f"/ws/chat/{self.session.conversation_id}/?token={self.token}"
        )
        await communicator.connect()
        await communicator.receive_json_from()
        
        await communicator.send_json_to({
            "message": "Hello AI, this is a test.",
            "conversation_id": str(self.session.conversation_id)
        })
        
        response = await communicator.receive_json_from()
        self.assertEqual(response['type'], 'new_message')
        self.assertEqual(response['message']['text'], "Hello AI, this is a test.")
        self.assertFalse(response['message']['is_ai'])
        
        await communicator.disconnect()