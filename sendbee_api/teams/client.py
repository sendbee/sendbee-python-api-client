from sendbee_api.teams import models
from sendbee_api.bind import bind_request
from sendbee_api.teams import query_params


class Teams:
    """Api client for conversations"""

    teams = bind_request(
        api_path='/teams/teams',
        model=models.Team,
        query_parameters=query_params.ListTeams,
        description='Api client for teams'
    )
    members = bind_request(
        api_path='/teams/members',
        model=models.Member,
        query_parameters=query_params.ListTeamMembers,
        description='Api client for team members'
    )
