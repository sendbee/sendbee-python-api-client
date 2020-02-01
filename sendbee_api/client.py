import click

from sendbee_api.auth import SendbeeAuth
from sendbee_api.contacts.client import Contacts
from sendbee_api.messages.client import Messages
from sendbee_api.exceptions import SendbeeRequestApiException


class Client(Contacts, Messages):
    """Main API class. Sets all API calls."""

    base_url = 'api-v1.sendbee.io'
    protocol = 'https'

    def __init__(self, api_key: str, secret: str, business_id: str = None,
                 debug: bool = False, fake_response_path: str = None):

        if not api_key:
            raise SendbeeRequestApiException('API key missing!')
        if not secret:
            raise SendbeeRequestApiException('API secret key missing!')

        self.debug = debug
        self.request = None
        self.secret = secret
        self.api_key = api_key
        self.business_id = business_id
        self.fake_response_path = fake_response_path

    @classmethod
    def print_params_for(cls, fn_name: str) -> None:
        """Prints parameters for certain API call function."""

        try:
            getattr(cls, fn_name)(None, print_params=True)
        except AttributeError:
            click.secho('Unknown API method: {}'.format(fn_name), fg='red')

    @property
    def auth(self):
        return SendbeeAuth(self.secret)
