from sendbee_api.query_params import QueryParams


class ListContacts(QueryParams):
    """Get the list of business' contacts"""

    tags = 'tags', 'Filter contacts by tags'
    search_query = 'search_query', 'Filter contacts by query string'


class SubscribeContacts(QueryParams):
    """Subscribe a contact to your business"""

    phone = 'phone', 'Contact phone number'
    tags = 'tags', 'Tag contact while subscribing it'
