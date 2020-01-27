from sendbee_api import constants
from sendbee_api.bind import bind_request

from sendbee_api.contacts.models import Contact
from sendbee_api.contacts.query_params import ListContacts


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
