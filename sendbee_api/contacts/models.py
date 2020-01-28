from sendbee_api.models import Model
from sendbee_api.fields import TextField, DatetimeField, ModelField


class ContactTag(Model):
    """Data model for contact tags"""

    _id = TextField(index='id', desc="UUID")
    _name = TextField(index='name', desc="Name")


class Contact(Model):
    """Data model for contacts"""

    _id = TextField(index='id', desc="UUID")
    _name = TextField(index='name', desc="Name")
    _phone = TextField(index='phone', desc="Phone number")
    _email = TextField(index='email', desc="Email address")
    _created_at = DatetimeField(
        index='created_at', desc="Name", format='%Y-%m-%d %H:%M:%S'
    )
    _tags = ModelField(ContactTag, index='tags', desc="Tags")
