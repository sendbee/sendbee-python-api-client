from sendbee_api.models import Model
from sendbee_api.fields import (
    TextField, BooleanField, DatetimeField, ListField
)


class Webhook(Model):
    """Data model for a webhook endpoint subscription"""

    _id = TextField(index='id', desc='UUID')
    _url = TextField(index='url', desc='Webhook endpoint URL')
    _active = BooleanField(index='active', desc='Is the endpoint active')
    _secret_key = TextField(
        index='secret_key',
        desc='Key that signs the X-Auth-Token header on inbound webhooks'
    )
    _selected_webhooks = ListField(
        index='selected_webhooks', desc='Subscribed webhook event names'
    )
    _created_at = DatetimeField(
        index='created_at', desc='Created at', format='%Y-%m-%d %H:%M:%'
    )
