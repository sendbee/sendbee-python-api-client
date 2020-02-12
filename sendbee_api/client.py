import click

from sendbee_api.auth import SendbeeAuth
from sendbee_api.contacts.client import Contacts
from sendbee_api.convresations.client import Messages
from sendbee_api.automation.client import Automation
from sendbee_api.exceptions import SendbeeRequestApiException


class Client(Contacts, Messages, Automation):
    """Main API class. Sets all API calls."""

    base_url = 'api-v2.sendbee.io'
    protocol = 'https'

    def __init__(self, secret, business_id=None,
                 debug=False, fake_response_path=None):

        if not secret:
            raise SendbeeRequestApiException('API secret key missing!')

        self.debug = debug
        self.request = None
        self.secret = secret
        self.business_id = business_id
        self.fake_response_path = fake_response_path

    @classmethod
    def print_params_for(cls, fn_name) -> None:
        """Prints parameters for certain API call function."""

        try:
            getattr(cls, fn_name)(None, print_params=True)
        except AttributeError:
            click.secho('Unknown API method: {}'.format(fn_name), fg='red')

    @property
    def auth(self):
        return SendbeeAuth(self.secret)
