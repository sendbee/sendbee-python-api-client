from sendbee_api.models import Model
from sendbee_api.fields import TextField, DatetimeField, ModelField, ListField


class ContactTag(Model):
    """Data model for contact tags"""

    _id = TextField(index='id', desc='UUID')
    _name = TextField(index='name', desc='Name')


class ContactField(Model):
    """Data model for contact contact fields"""

    _id = TextField(index='id', desc='Field UUID')
    _type = TextField(index='type', desc='Type')
    _name = TextField(index='name', desc='Name')
    _options = ListField(index='options', desc='List type options')


class Note(Model):
    """Data model for contact notes"""

    _note = TextField(index='note', desc='Note')


class ContactContactField(Model):
    """Data model for contact contact fields"""

    _key = TextField(index='key', desc='Contact field key')
    _value = TextField(index='value', desc='Contact field value')


class ContactNote(Model):
    """Data model for contact notes"""

    _value = TextField(index='value', desc='Note value')


class Contact(Model):
    """Data model for contacts"""

    _id = TextField(index='id', desc='UUID')
    _name = TextField(index='name', desc='Name')
    _phone = TextField(index='phone', desc='Phone number')
    _created_at = DatetimeField(
        index='created_at', desc='Name', format='%Y-%m-%d %H:%M:%'
    )
    _tags = ModelField(ContactTag, index='tags', desc='Tags')
    _status = TextField(index='status', desc='Subscription status')
    _folder = TextField(index='folder', desc='Conversation folder')
    _contact_fields = ModelField(
        ContactContactField, index='contact_fields', desc='Contact field'
    )
    _notes = ModelField(ContactNote, index='notes', desc='Notes')
