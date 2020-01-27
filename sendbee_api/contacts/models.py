from sendbee_api.models import Model
from sendbee_api.fields import TextField, DatetimeField, ModelField


class ContactTag(Model):
    """Data model for contact tags"""

    name = TextField(index='name', desc="Name")


class Contact(Model):
    """Data model for contacts"""

    id = TextField(index='id', desc="UUID")
    name = TextField(index='name', desc="Name")
    phone = TextField(index='phone', desc="Phone number")
    email = TextField(index='email', desc="Email address")
    created_at = DatetimeField(
        index='created_at', desc="Name", format='%Y-%m-%d %H:%M:%S'
    )
    tags = ModelField(ContactTag, index='tags', desc="Tags")
