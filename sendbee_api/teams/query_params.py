from sendbee_api.query_params import QueryParams


class ListTeams(QueryParams):
    """Parameters for list of teams"""

    member_id = 'member_id', 'Fetch teams for a member'


class ListTeamMembers(QueryParams):
    """Parameters for list of team members"""

    team_id = 'team_id', 'Fetch members of one team'
