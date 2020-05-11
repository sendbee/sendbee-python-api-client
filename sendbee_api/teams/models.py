from sendbee_api.models import Model
from sendbee_api.fields import TextField, ModelField, BooleanField


class MemberTeam(Model):
    """Data model for member team"""

    _id = TextField(index='id', desc='UUID')
    _name = TextField(index='name', desc='Name')


class Member(Model):
    """Data model for member"""

    _id = TextField(index='id', desc='UUID')
    _name = TextField(index='name', desc='Name')
    _role = TextField(index='role', desc='Role')
    _online = TextField(index='online', desc='Online')
    _available = TextField(index='available', desc='Available')
    _teams = ModelField(MemberTeam, index='teams', desc='Teams')


class TeamMember(Model):
    """Data model for team team member"""

    _id = TextField(index='id', desc='UUID')
    _name = TextField(index='name', desc='Name')
    _role = TextField(index='role', desc='Role')
    _online = TextField(index='online', desc='Online')
    _available = TextField(index='available', desc='Available')


class Team(Model):
    """Data model for team"""

    _id = TextField(index='id', desc='UUID')
    _name = TextField(index='name', desc='Name')
    _members = ModelField(TeamMember, index='members', desc='Members')
