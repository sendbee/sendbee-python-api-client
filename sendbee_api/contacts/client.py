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
    custom_fields = bind_request(
        api_path='/contacts/custom-fields',
        model=models.CustomField,
        query_parameters=query_params.ListCustomFields,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for custom fields'
    )
    create_custom_field = bind_request(
        api_path='/contacts/custom-fields',
        model=models.CustomField,
        method=constants.RequestConst.POST,
        query_parameters=query_params.CreateCustomFields,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for creating contact custom fields'
    )
    update_custom_field = bind_request(
        api_path='/contacts/custom-fields',
        model=models.CustomField,
        method=constants.RequestConst.PUT,
        query_parameters=query_params.UpdateCustomFields,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for updating contact custom fields'
    )
    delete_custom_field = bind_request(
        api_path='/contacts/custom-fields',
        model=ServerMessage,
        method=constants.RequestConst.DELETE,
        query_parameters=query_params.DeleteCustomFields,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for deleting contact custom fields'
    )
