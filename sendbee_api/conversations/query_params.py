from sendbee_api.query_params import QueryParams


class ListMessageTemplates(QueryParams):
    """Parameters for list of message templates API request"""

    status = 'status', 'Fetch templates with desired status'
    search_query = 'search_query', 'Filter contacts by query string'
    page = 'page', 'Page number for pagination'
    limit = 'limit', 'Number of items per page. Maximum is 100.'


class SendTemplateMessage(QueryParams):
    """Parameters for sending template message"""

    tags = 'tags', 'Template message tags'
    button_tags = 'button_tags', 'Template button tags'
    phone = 'phone', 'Contact\'s phone number'
    language = 'language', 'Template message language'
    template_keyword = 'template_keyword', 'Template message keyword'
    prevent_bot_off = 'prevent_bot_off', 'Prevent turning-off chatbot'
    agent_id = 'agent_id', 'Assigned agent for the conversation'
    attachment = 'attachment', 'Attachment URL for media templates'


class SendMessage(QueryParams):
    """Parameters for sending message"""

    phone = 'phone', 'Contact\'s phone number'
    text = 'text', 'Message text'
    media_url = 'media_url', 'Media URL for media message'
    prevent_bot_off = 'prevent_bot_off', 'Prevent turning-off chatbot'
    agent_id = 'agent_id', 'Assigned agent for the conversation'


class ListConversations(QueryParams):
    """Parameters for list of conversations"""

    date_from = 'date_from', 'Fetch all conversations from this date'
    date_to = 'date_to', 'Fetch all conversations to this date'
    folder = 'folder', 'Filter conversation by folder'
    search_query = 'search_query', 'Filter conversations by query string'
    page = 'page', 'Page number for pagination'
    limit = 'limit', 'Number of items per page. Maximum is 100.'


class ListMessages(QueryParams):
    """Parameters for list of messages"""

    conversation_id = 'conversation_id', 'Conversation UUID'
    page = 'page', 'Page number for pagination'


class GetSingleConversation(QueryParams):
    """Parameters for getting a single conversation"""
    conversation_id = 'conversation_id', 'Conversation UUID'


class UpdateSingleConversation(QueryParams):
    """Parameters for updating a single conversation"""
    conversation_id = 'conversation_id', 'Conversation UUID'
    folder = 'folder', 'Assign conversation to specific folder, open|done'
