from sendbee_api import constants
from sendbee_api.bind import bind_request

from sendbee_api.models import ServerMessage
from sendbee_api.constants import RequestConst
from sendbee_api.contacts.models import Contact, ContactTag
from sendbee_api.contacts.query_params import ListContacts, SubscribeContacts, \
    ListTags, UpdateTag, DeleteTag


class Contacts:
    """Api client for contacts"""

    contacts = bind_request(
        api_path='/contacts',
        model=Contact,
        query_parameters=ListContacts,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for contacts'
    )
    subscribe_contact = bind_request(
        api_path='/contacts/subscribe',
        model=Contact,
        method=RequestConst.POST,
        query_parameters=SubscribeContacts,
        default_parameters={
            constants.RequestConst.BLOCK_NOTIFICATIONS: 'yes',
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for subscribing contacts'
    )
    tags = bind_request(
        api_path='/contacts/tags',
        model=ContactTag,
        query_parameters=ListTags,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for tags'
    )
    update_tag = bind_request(
        api_path='/contacts/tags',
        model=ContactTag,
        method=RequestConst.PUT,
        query_parameters=UpdateTag,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for updating tags'
    )
    create_tag = bind_request(
        api_path='/contacts/tags',
        model=ContactTag,
        method=RequestConst.POST,
        query_parameters=ListTags,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for updating tags'
    )
    delete_tag = bind_request(
        api_path='/contacts/tags',
        model=ServerMessage,
        method=RequestConst.DELETE,
        query_parameters=DeleteTag,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for deleting tags'
    )
