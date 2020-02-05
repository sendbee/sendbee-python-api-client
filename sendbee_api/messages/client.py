from sendbee_api import constants
from sendbee_api.messages import models
from sendbee_api.bind import bind_request
from sendbee_api.messages import query_params


class Messages:
    """Api client for messages"""

    message_templates = bind_request(
        api_path='/message/templates',
        model=models.MessageTemplate,
        query_parameters=query_params.ListMessageTemplates,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for message templates'
    )
    send_template_message = bind_request(
        api_path='/message/templates/send',
        model=models.SentMessage,
        method=constants.RequestConst.POST,
        query_parameters=query_params.SendMessage,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for sending template messages'
    )
