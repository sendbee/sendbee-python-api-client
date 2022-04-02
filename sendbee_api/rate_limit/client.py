from sendbee_api import constants
from sendbee_api.bind import bind_request
from sendbee_api.rate_limit import query_params
from sendbee_api.rate_limit.models import RateLimitError


class RateLimit:
    """Api client for rete limit testing"""

    rate_limit_error_test = bind_request(
        api_path='/rate-limit/error-test',
        model=RateLimitError,
        query_parameters=query_params.RateLimitParams,
        method=constants.RequestConst.GET,
        # ignore_error=True,
        description='Rate limit error test'
    )

    rate_limit_request_test = bind_request(
        api_path='/rate-limit/request-test',
        model=RateLimitError,
        query_parameters=query_params.RateLimitParams,
        method=constants.RequestConst.GET,
        # ignore_error=True,
        description='Rate limit request test'
    )
