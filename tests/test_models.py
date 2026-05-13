"""Tests for Model.process(): attribute translation and nested model recursion."""

from sendbee_api.models import Model, Meta, ServerMessage
from sendbee_api.fields import TextField, NumberField, ModelField


class _Tag(Model):
    _name = TextField(index="name")


class _Contact(Model):
    _id = TextField(index="id")
    _name = TextField(index="name")
    _tags = ModelField(_Tag, index="tags")


class _Wrapper(Model):
    _label = TextField(index="label")
    _tag = ModelField(_Tag, index="tag")


def test_process_strips_leading_underscore_from_class_attr_when_exposing_on_instance():
    """`_name` on the class becomes `name` on the instance after process()."""
    [contact] = _Contact.process([{"id": "c1", "name": "Alice", "tags": []}])

    assert contact.id == "c1"
    assert contact.name == "Alice"


def test_process_returns_list_of_model_instances_one_per_input_dict():
    """process() returns one Model per input record."""
    contacts = _Contact.process([
        {"id": "c1", "name": "Alice", "tags": []},
        {"id": "c2", "name": "Bob", "tags": []},
    ])

    assert len(contacts) == 2
    assert [c.id for c in contacts] == ["c1", "c2"]


def test_process_recurses_into_model_field_when_value_is_list():
    """List-valued ModelField is mapped element-wise into nested models."""
    [contact] = _Contact.process([{
        "id": "c1",
        "name": "Alice",
        "tags": [{"name": "vip"}, {"name": "lead"}],
    }])

    assert isinstance(contact.tags, list)
    assert [t.name for t in contact.tags] == ["vip", "lead"]


def test_process_recurses_into_model_field_when_value_is_dict():
    """Dict-valued ModelField is mapped to a single nested model (not a list)."""
    [wrapper] = _Wrapper.process([{"label": "x", "tag": {"name": "vip"}}])

    assert not isinstance(wrapper.tag, list)
    assert wrapper.tag.name == "vip"


def test_process_sets_attribute_to_none_when_source_value_is_none():
    """A None field value is preserved as None on the instance."""
    [contact] = _Contact.process([{"id": "c1", "name": None, "tags": []}])

    assert contact.name is None


def test_getattr_raises_attribute_error_for_unknown_attribute():
    """Accessing an attribute that was never declared raises AttributeError."""
    [contact] = _Contact.process([{"id": "c1", "name": "Alice", "tags": []}])

    try:
        _ = contact.does_not_exist
    except AttributeError:
        return
    raise AssertionError("expected AttributeError")


def test_meta_model_exposes_pagination_fields_as_ints():
    """Meta.process maps current/last/per/total fields to ints."""
    [meta] = Meta.process([{
        "total": "100",
        "to": "20",
        "from": "1",
        "per_page": "20",
        "last_page": "5",
        "current_page": "1",
    }])

    assert meta.total == 100
    assert meta.last_page == 5
    assert meta.current_page == 1


def test_server_message_exposes_message_field():
    """ServerMessage carries a single `message` text field."""
    [sm] = ServerMessage.process([{"message": "deleted"}])

    assert sm.message == "deleted"
