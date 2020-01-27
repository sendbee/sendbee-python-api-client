from sendbee_api import constants
from sendbee_api.bind import bind_request

from sendbee_api.messages.models import MessageTemplate
from sendbee_api.messages.query_params import ListMessageTemplates


class Messages:
    """Api client for messages"""

    message_templates = bind_request(
        api_path='/message-templates',
        model=MessageTemplate,
        query_parameters=ListMessageTemplates,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for messages'
    )
