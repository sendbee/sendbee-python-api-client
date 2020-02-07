from sendbee_api.constants import RequestConst
from sendbee_api.query_params import QueryParams


class ListContacts(QueryParams):
    """Get the list of business' contacts"""

    tags = 'tags', 'Filter contacts by tags'
    search_query = 'search_query', 'Filter contacts by query string'


class UpdateContacts(QueryParams):
    """Update a contact"""

    id = 'id', 'Contact ID'
    phone = 'phone', 'Contact phone number'
    tags = 'tags', 'Tag contact while subscribing it'
    name = 'name', 'Subscriber name'
    email = 'email', 'Subscriber email'
    address = 'address', 'Subscriber address'
    contact_fields = 'contact_fields', 'Contact data fields'
    facebook_link = 'facebook_link', 'Subscriber Facebook link'
    twitter_link = 'twitter_link', 'Subscriber Twitter link'
    notes = 'notes', 'Notes about subscriber'
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


class ListContactFields(QueryParams):
    """Get the list of contact contact fields"""

    search_query = 'search_query', 'Filter contact contact fields by query string'


class CreateContactFields(QueryParams):
    """Create contact contact fields"""

    name = 'name', 'Name of the contact field'
    type = 'type', 'Type of the contact field'


class UpdateContactFields(QueryParams):
    """Update contact contact fields"""

    slug = 'slug', 'Slug of the contact field'
    name = 'name', 'Name of the contact field'
    type = 'type', 'Type of the contact field'


class DeleteContactFields(QueryParams):
    """Delete tag"""

    slug = 'slug', 'Contact field tag'
