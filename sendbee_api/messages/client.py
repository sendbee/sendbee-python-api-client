from sendbee_api import constants
from sendbee_api.bind import bind_request

from sendbee_api.constants import RequestConst
from sendbee_api.messages.models import MessageTemplate, SentMessage
from sendbee_api.messages.query_params import ListMessageTemplates, SendMessage


class Messages:
    """Api client for messages"""

    message_templates = bind_request(
        api_path='/message/templates',
        model=MessageTemplate,
        query_parameters=ListMessageTemplates,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for message templates'
    )
    send_template_message = bind_request(
        api_path='/message/templates/send',
        model=SentMessage,
        method=RequestConst.POST,
        query_parameters=SendMessage,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for sending template messages'
    )
