from sendbee_api.constants import RequestConst
from sendbee_api.query_params import QueryParams


class ListContacts(QueryParams):
    """Get the list of business' contacts"""

    tags = 'tags', 'Filter contacts by tags'
    status = 'status', 'Filter contacts by status'
    search_query = 'search_query', 'Filter contacts by query string'
    page = 'page', 'Page number for pagination'


class UpdateContacts(QueryParams):
    """Update a contact"""

    id = 'id', 'Contact ID'
    phone = 'phone', 'Contact phone number'
    tags = 'tags', 'Tag contact while subscribing it'
    name = 'name', 'Subscriber name'
    contact_fields = 'contact_fields', 'Contact data fields'
    notes = 'notes', 'Notes about subscriber'
    block_notifications = RequestConst.BLOCK_NOTIFICATIONS, \
                          'Block sending notifications ' \
                          'after subscribing contact'


class ListTags(QueryParams):
    """Get the list of contact tags"""

    name = 'name', 'Name of the tag'
    page = 'page', 'Page number for pagination'


class UpdateTag(QueryParams):
    """Update tag"""

    id = 'id', 'ID of the tag'
    name = 'name', 'Name of the tag'


class DeleteTag(QueryParams):
    """Delete tag"""

    id = 'id', 'ID of the tag'


class ListContactFields(QueryParams):
    """Get the list of contact contact fields"""

    page = 'page', 'Page number for pagination'
    search_query = 'search_query', 'Filter contact contact ' \
                                   'fields by query string'


class CreateContactFields(QueryParams):
    """Create contact contact fields"""

    name = 'name', 'Name of the contact field'
    type = 'type', 'Type of the contact field'
    options = 'options', 'List type options'


class UpdateContactFields(QueryParams):
    """Update contact contact fields"""

    id = 'id', 'Contact field UUID'
    name = 'name', 'Name of the contact field'
    type = 'type', 'Type of the contact field'
    options = 'options', 'List type options'


class DeleteContactFields(QueryParams):
    """Delete tag"""

    id = 'id', 'Contact field UUID'
