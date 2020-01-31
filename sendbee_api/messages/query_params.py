from sendbee_api.query_params import QueryParams


class ListMessageTemplates(QueryParams):
    """Parameters for list of message templates API request"""

    search_query = 'search_query', 'Filter contacts by query string'


class SendMessage(QueryParams):
    """Parameters for sending template message"""

    tags = 'tags', 'Template message tags'
    phone = 'phone', 'Contact\'s phone number'
    language = 'language', 'Template message language'
    template_keyword = 'template_keyword', 'Template message keyword'
