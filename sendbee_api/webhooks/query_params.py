from sendbee_api.query_params import QueryParams


class SubscribeWebhook(QueryParams):
    """Parameters for subscribing to a webhook event"""

    url = 'url', 'Webhook endpoint URL that will receive the events'
    event = 'event', 'Webhook event name, e.g. "message.received". ' \
                     'See https://developer.ainumber.com/#webhooks'
