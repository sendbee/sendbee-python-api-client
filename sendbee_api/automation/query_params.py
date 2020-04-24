from sendbee_api.query_params import QueryParams


class ChatbotActivity(QueryParams):
    """Parameters for turning the chatbot on or off for a conversation"""

    conversation_id = 'conversation_id', 'Conversation UUID'
    active = 'active', 'Chatbot activity'

class ChatbotActivityStatus(QueryParams):
    """Parameters for getting chatbot status for a conversation"""

    conversation_id = 'conversation_id', 'Conversation UUID'
