from sendbee_api.query_params import QueryParams


class ListMessageTemplates(QueryParams):
    """Get the list of message templates"""

    search_query = 'search_query', 'Filter contacts by query string'
