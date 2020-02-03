from sendbee_api.constants import RequestConst
from sendbee_api.query_params import QueryParams


class ListContacts(QueryParams):
    """Get the list of business' contacts"""

    tags = 'tags', 'Filter contacts by tags'
    search_query = 'search_query', 'Filter contacts by query string'


class SubscribeContacts(QueryParams):
    """Subscribe a contact to your business"""

    phone = 'phone', 'Contact phone number'
    tags = 'tags', 'Tag contact while subscribing it'
    block_notifications = RequestConst.BLOCK_NOTIFICATIONS, \
                          'Block sending notifications after subscribing contact'


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


class ListCustomFields(QueryParams):
    """Get the list of contact custom fields"""

    search_query = 'search_query', 'Filter contact custom fields by query string'


class CreateCustomFields(QueryParams):
    """Create contact custom fields"""

    name = 'name', 'Name of the custom field'
    type = 'type', 'Type of the custom field'


class UpdateCustomFields(QueryParams):
    """Update contact custom fields"""

    slug = 'slug', 'Slug of the custom field'
    name = 'name', 'Name of the custom field'
    type = 'type', 'Type of the custom field'


class DeleteCustomFields(QueryParams):
    """Delete tag"""

    slug = 'slug', 'Custom field tag'
