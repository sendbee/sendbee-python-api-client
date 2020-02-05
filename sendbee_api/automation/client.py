from sendbee_api import constants
from sendbee_api.bind import bind_request
# from sendbee_api.automation import models
from sendbee_api.models import ServerMessage
from sendbee_api.automation import query_params


class Automation:
    """Api client for automation"""

    bot_on = bind_request(
        api_path='/automation/toggle-bot',
        model=ServerMessage,
        query_parameters=query_params.TootleBotOnOff,
        method=constants.RequestConst.PUT,
        default_parameters={
            constants.AutomationConst.TOGGLE_BOT: True,
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for turning the automation bot on'
    )
    bot_off = bind_request(
        api_path='/automation/toggle-bot',
        model=ServerMessage,
        query_parameters=query_params.TootleBotOnOff,
        method=constants.RequestConst.PUT,
        default_parameters={
            constants.AutomationConst.TOGGLE_BOT: False,
            constants.RequestConst.PROTOCOL: constants.FormatterConst.JSON
        },
        description='Api client for turning the automation bot off'
    )
