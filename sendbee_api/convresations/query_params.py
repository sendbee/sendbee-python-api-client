from sendbee_api.query_params import QueryParams


class ListMessageTemplates(QueryParams):
    """Parameters for list of message templates API request"""

    search_query = 'search_query', 'Filter contacts by query string'


class SendTemplateMessage(QueryParams):
    """Parameters for sending template message"""

    tags = 'tags', 'Template message tags'
    phone = 'phone', 'Contact\'s phone number'
    language = 'language', 'Template message language'
    template_keyword = 'template_keyword', 'Template message keyword'


class SendMessage(QueryParams):
    """Parameters for sending message"""

    phone = 'phone', 'Contact\'s phone number'
    text = 'text', 'Message text'
    media_url = 'media_url', 'Media URL for media message'


class ListConversations(QueryParams):
    """Parameters for list of conversations"""

    folder = 'folder', 'Filter conversation by folder'
    search_query = 'search_query', 'Filter conversations by query string'


class ListMessages(QueryParams):
    """Parameters for list of messages"""

    conversation_id = 'conversation_id', 'Conversation UUID'
