from sendbee_api import constants
from sendbee_api.conversations import models
from sendbee_api.bind import bind_request
from sendbee_api.conversations import query_params


class Messages:
    """Api client for conversations"""

    message_templates = bind_request(
        api_path='/conversations/messages/templates',
        model=models.MessageTemplate,
        query_parameters=query_params.ListMessageTemplates,
        description='Api client for message templates'
    )
    send_template_message = bind_request(
        api_path='/conversations/messages/templates/send',
        model=models.SentMessage,
        method=constants.RequestConst.POST,
        query_parameters=query_params.SendTemplateMessage,
        description='Api client for sending template conversations'
    )
    send_message = bind_request(
        api_path='/conversations/messages/send',
        model=models.SentMessage,
        method=constants.RequestConst.POST,
        query_parameters=query_params.SendMessage,
        description='Api client for sending template conversations'
    )
    conversations = bind_request(
        api_path='/conversations',
        model=models.Conversation,
        query_parameters=query_params.ListConversations,
        description='Api client for fetching conversations'
    )
    messages = bind_request(
        api_path='/conversations/messages',
        model=models.Message,
        query_parameters=query_params.ListMessages,
        description='Api client for fetching conversation messages'
    )

    get_conversation = bind_request(
        api_path='/conversation',
        query_parameters=query_params.GetSingleConversation,
        model=models.Conversation,
        force_single_model_response=True,
        description='Api client for fetching single conversation data'
    )
    update_conversation = bind_request(
        api_path='/conversation',
        method=constants.RequestConst.POST,
        query_parameters=query_params.UpdateSingleConversation,
        model=models.Conversation,
        force_single_model_response=True,
        # query_parameters=query_params.ListMessages,
        description='Api client for updating a conversation'
    )
