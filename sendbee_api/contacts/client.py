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
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
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
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for subscribing a contacts'
    )
    update_contact = bind_request(
        api_path='/contacts',
        model=models.Contact,
        method=constants.RequestConst.PUT,
        query_parameters=query_params.UpdateContacts,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for updating contacts'
    )
    tags = bind_request(
        api_path='/contacts/tags',
        model=models.ContactTag,
        query_parameters=query_params.ListTags,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for tags'
    )
    update_tag = bind_request(
        api_path='/contacts/tags',
        model=models.ContactTag,
        method=constants.RequestConst.PUT,
        query_parameters=query_params.UpdateTag,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for updating tags'
    )
    create_tag = bind_request(
        api_path='/contacts/tags',
        model=models.ContactTag,
        method=constants.RequestConst.POST,
        query_parameters=query_params.ListTags,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for updating tags'
    )
    delete_tag = bind_request(
        api_path='/contacts/tags',
        model=ServerMessage,
        method=constants.RequestConst.DELETE,
        query_parameters=query_params.DeleteTag,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for deleting tags'
    )
    contact_fields = bind_request(
        api_path='/contacts/contact-fields',
        model=models.ContactField,
        query_parameters=query_params.ListContactFields,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for contact fields'
    )
    create_contact_field = bind_request(
        api_path='/contacts/contact-fields',
        model=models.ContactField,
        method=constants.RequestConst.POST,
        query_parameters=query_params.CreateContactFields,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for creating contact contact fields'
    )
    update_contact_field = bind_request(
        api_path='/contacts/contact-fields',
        model=models.ContactField,
        method=constants.RequestConst.PUT,
        query_parameters=query_params.UpdateContactFields,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for updating contact contact fields'
    )
    delete_contact_field = bind_request(
        api_path='/contacts/contact-fields',
        model=ServerMessage,
        method=constants.RequestConst.DELETE,
        query_parameters=query_params.DeleteContactFields,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for deleting contact contact fields'
    )
