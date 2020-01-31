from sendbee_api.models import Model
from sendbee_api.fields import TextField, ModelField, BooleanField


class TamplateTag(Model):
    """Data model for template tags"""

    _name = TextField(index='name', desc="Name")


class MessageTemplate(Model):
    """Data model for message templates"""

    _id = TextField(index='id', desc="UUID")
    _approved = BooleanField(index='approved', desc="Approved")
    _keyword = TextField(index='keyword', desc="Keyword")
    _tags = ModelField(TamplateTag, index='tags', desc="Tags")
    _text = TextField(index='text', desc="Text")
    _language = TextField(index='language', desc="Language")


class SentMessage(Model):
    """Data model for sent message"""

    _conversation_id = TextField(index='id', desc="Message UUID")
