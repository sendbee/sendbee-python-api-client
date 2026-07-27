from sendbee_api import constants
from sendbee_api.webhooks import models
from sendbee_api.bind import bind_request
from sendbee_api.webhooks import query_params


class Webhooks:
    """Api client for webhooks"""

    subscribe_webhook = bind_request(
        api_path='/webhooks/subscribe',
        model=models.Webhook,
        method=constants.RequestConst.POST,
        query_parameters=query_params.SubscribeWebhook,
        description='Api client for subscribing to a webhook event'
    )
