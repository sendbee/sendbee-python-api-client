from sendbee_api.models import Model
from sendbee_api.fields import TextField, ModelField, BooleanField, \
    DatetimeField


class TamplateTag(Model):
    """Data model for template tags"""

    _name = TextField(index='name', desc='Name')


class MessageTemplate(Model):
    """Data model for message templates"""

    _id = TextField(index='id', desc='UUID')
    _approved = BooleanField(index='approved', desc='Approved')
    _keyword = TextField(index='keyword', desc='Keyword')
    _tags = ModelField(TamplateTag, index='tags', desc='Tags')
    _text = TextField(index='text', desc='Text')
    _language = TextField(index='language', desc='Language')


class SentMessage(Model):
    """Data model for sent message"""

    _conversation_id = TextField(index='id', desc='Message UUID')


class ConversationContact(Model):
    """Data model for contact in conversation"""

    _id = TextField(index='id', desc='UUID')
    _name = TextField(index='name', desc='Name')
    _phone = TextField(index='phone', desc='Phone number')


class ConversationLastMessage(Model):
    """Data model for contact in conversation"""

    _direction = TextField(index='direction', desc='Last message direction')
    _status = TextField(index='status', desc='Last message status')
    _inbound_sent_at = DatetimeField(
        index='inbound_sent_at', desc='Last inbound message sent at',
        format='%Y-%m-%d %H:%M:%'
    )
    _outbound_sent_at = DatetimeField(
        index='outbound_sent_at', desc='Last outbound message sent at',
        format='%Y-%m-%d %H:%M:%'
    )


class Conversation(Model):
    """Data model for conversations"""

    _id = TextField(index='id', desc='UUID')
    _folder = TextField(index='folder', desc='Folder')
    _last_message = ModelField(
        ConversationLastMessage, index='last_message', desc='Last message'
    )
    _contact = ModelField(ConversationContact, index='contact', desc='Contact')
    _chatbot_active = BooleanField(index='chatbot_active', desc='Approved')
    _platform = BooleanField(index='platform', desc='Platform')
    _created_at = DatetimeField(
        index='created_at', desc='Created at', format='%Y-%m-%d %H:%M:%'
    )


class Message(Model):
    """Data model for messages"""

    _type = TextField(index='type', desc='Message type')
    _body = TextField(index='body', desc='Message body')
    _media_type = TextField(index='media_type', desc='Message media type')
    _media_url = TextField(index='media_url', desc='Media URL')
    _status = TextField(index='status', desc='Message status')
    _direction = TextField(index='direction', desc='Message direction')
    _sent_at = DatetimeField(
        index='sent_at', desc='Message sent at', format='%Y-%m-%d %H:%M:%'
    )
