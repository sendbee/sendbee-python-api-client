from sendbee_api import constants
from sendbee_api.bind import bind_request
from sendbee_api.models import ServerMessage
from sendbee_api.automation.models import ChatbotActivityStatus
from sendbee_api.automation import query_params


class Automation:
    """Api client for automation"""

    chatbot_activity = bind_request(
        api_path='/automation/chatbot/activity',
        model=ServerMessage,
        query_parameters=query_params.ChatbotActivity,
        method=constants.RequestConst.PUT,
        description='Api client for turning the '
                    'chatbot on or off for a conversation'
    )

    chatbot_activity_status = bind_request(
        api_path='/automation/chatbot/activity/status',
        model=ChatbotActivityStatus,
        force_single_model_response=True,
        query_parameters=query_params.ChatbotActivityStatus,
        method=constants.RequestConst.GET,
        description='Api client for getting current '
                    'chatbot status for a conversation'
    )
