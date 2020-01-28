from sendbee_api.query_params import QueryParams


class ListContacts(QueryParams):
    """Get the list of business' contacts"""

    tags = 'tags', 'Filter contacts by tags'
    search_query = 'search_query', 'Filter contacts by query string'


class SubscribeContacts(QueryParams):
    """Subscribe a contact to your business"""

    phone = 'phone', 'Contact phone number'
    tags = 'tags', 'Tag contact while subscribing it'


class ListTags(QueryParams):
    """Get the list of contact tags"""

    name = 'name', 'Name of the tag'


class UpdateTag(QueryParams):
    """Update tag"""

    id = 'id', 'ID of the tag'
    name = 'name', 'Name of the tag'


class DeleteTag(QueryParams):
    """Delete tag"""

    id = 'id', 'ID of the tag'
