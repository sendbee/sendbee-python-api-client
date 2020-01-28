from sendbee_api import constants
from sendbee_api.bind import bind_request

from sendbee_api.constants import RequestConst
from sendbee_api.contacts.models import Contact
from sendbee_api.contacts.query_params import ListContacts, SubscribeContacts


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
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for contacts'
    )
