from sendbee_api.models import Model
from sendbee_api.fields import TextField, BooleanField

class ChatbotActivityStatus(Model):
    """Data model for chatbot status"""

    _conversation_id = TextField(index='conversation_id', desc='Conversation UUID')
    _chatbot_active = BooleanField(index='chatbot_active', desc='Chatbot status')
