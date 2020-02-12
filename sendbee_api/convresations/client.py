from sendbee_api import constants
from sendbee_api.convresations import models
from sendbee_api.bind import bind_request
from sendbee_api.convresations import query_params


class Messages:
    """Api client for convresations"""

    message_templates = bind_request(
        api_path='/conversations/messages/templates',
        model=models.MessageTemplate,
        query_parameters=query_params.ListMessageTemplates,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for message templates'
    )
    send_template_message = bind_request(
        api_path='/conversations/messages/templates/send',
        model=models.SentMessage,
        method=constants.RequestConst.POST,
        query_parameters=query_params.SendTemplateMessage,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for sending template conversations'
    )
    send_message = bind_request(
        api_path='/conversations/messages/send',
        model=models.SentMessage,
        method=constants.RequestConst.POST,
        query_parameters=query_params.SendMessage,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for sending template conversations'
    )
    conversations = bind_request(
        api_path='/conversations',
        model=models.Conversation,
        query_parameters=query_params.ListConversations,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for fetching conversations'
    )
    messages = bind_request(
        api_path='/conversations/messages',
        model=models.Message,
        query_parameters=query_params.ListMessages,
        default_parameters={
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for fetching conversation messages'
    )
