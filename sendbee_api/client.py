import click

from sendbee_api.auth import SendbeeAuth
from sendbee_api.contacts.client import Contacts
from sendbee_api.conversations.client import Messages
from sendbee_api.automation.client import Automation
from sendbee_api.exceptions import SendbeeRequestApiException


class Client(Contacts, Messages, Automation):
    """Main API class. Sets all API calls."""

    base_url = 'api-v2.sendbee.io'
    protocol = 'https'

    def __init__(self, api_key, api_secret,
                 debug=False, fake_response_path=None):

        if not api_key:
            raise SendbeeRequestApiException('API key missing!')
        if not api_secret:
            raise SendbeeRequestApiException('API secret missing!')

        self.debug = debug
        self.request = None
        self.api_key = api_key
        self.api_secret = api_secret
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
        return SendbeeAuth(self.api_secret)
