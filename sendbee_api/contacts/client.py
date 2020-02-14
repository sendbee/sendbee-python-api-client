from sendbee_api import constants
from sendbee_api.contacts import models
from sendbee_api.bind import bind_request
from sendbee_api.models import ServerMessage
from sendbee_api.contacts import query_params


class Contacts:
    """Api client for contacts"""

    contacts = bind_request(
        api_path='/contacts',
        model=models.Contact,
        query_parameters=query_params.ListContacts,
        description='Api client for contacts'
    )
    subscribe_contact = bind_request(
        api_path='/contacts/subscribe',
        model=models.Contact,
        method=constants.RequestConst.POST,
        query_parameters=query_params.UpdateContacts,
        default_parameters={
            constants.RequestConst.BLOCK_AUTOMATION: True,
            constants.RequestConst.BLOCK_NOTIFICATIONS: True,
        },
        description='Api client for subscribing a contacts'
    )
    update_contact = bind_request(
        api_path='/contacts',
        model=models.Contact,
        method=constants.RequestConst.PUT,
        query_parameters=query_params.UpdateContacts,
        description='Api client for updating contacts'
    )
    tags = bind_request(
        api_path='/contacts/tags',
        model=models.ContactTag,
        query_parameters=query_params.ListTags,
        description='Api client for tags'
    )
    update_tag = bind_request(
        api_path='/contacts/tags',
        model=models.ContactTag,
        method=constants.RequestConst.PUT,
        query_parameters=query_params.UpdateTag,
        description='Api client for updating tags'
    )
    create_tag = bind_request(
        api_path='/contacts/tags',
        model=models.ContactTag,
        method=constants.RequestConst.POST,
        query_parameters=query_params.ListTags,
        description='Api client for updating tags'
    )
    delete_tag = bind_request(
        api_path='/contacts/tags',
        model=ServerMessage,
        method=constants.RequestConst.DELETE,
        query_parameters=query_params.DeleteTag,
        description='Api client for deleting tags'
    )
    contact_fields = bind_request(
        api_path='/contacts/fields',
        model=models.ContactField,
        query_parameters=query_params.ListContactFields,
        description='Api client for contact fields'
    )
    create_contact_field = bind_request(
        api_path='/contacts/fields',
        model=models.ContactField,
        method=constants.RequestConst.POST,
        query_parameters=query_params.CreateContactFields,
        description='Api client for creating contact contact fields'
    )
    update_contact_field = bind_request(
        api_path='/contacts/fields',
        model=models.ContactField,
        method=constants.RequestConst.PUT,
        query_parameters=query_params.UpdateContactFields,
        description='Api client for updating contact contact fields'
    )
    delete_contact_field = bind_request(
        api_path='/contacts/fields',
        model=ServerMessage,
        method=constants.RequestConst.DELETE,
        query_parameters=query_params.DeleteContactFields,
        description='Api client for deleting contact contact fields'
    )
