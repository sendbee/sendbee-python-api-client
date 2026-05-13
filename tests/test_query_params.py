"""Tests for QueryParams: MultiValueEnum aliasing and default merge."""

from sendbee_api.query_params import QueryParams, DefaultQueryParams


class _DemoParams(QueryParams):
    """Sample query param set for testing."""

    name = "name", "Contact name"
    search_query = "search_query", "Free text filter"


def test_get_params_returns_mapping_of_python_name_to_wire_name():
    """Python attribute names map to their wire-name strings."""
    params = _DemoParams.get_params()

    assert params["name"] == "name"
    assert params["search_query"] == "search_query"


def test_get_params_includes_default_query_params_for_msgtype_and_protocol():
    """DefaultQueryParams are merged in; msgtype/protocol available everywhere."""
    params = _DemoParams.get_params()

    assert "msg_type" in params
    assert params["msg_type"] == "msgtype"
    assert "protocol" in params


def test_multi_value_enum_resolves_both_tuple_values_to_same_member():
    """Looking up by wire-name or by description string yields the same member.

    aenum.MultiValueEnum allows any element of the tuple to be a valid lookup
    value, so members defined as `name = ('wire', 'desc')` can be retrieved by
    either string.
    """
    by_wire = DefaultQueryParams("msgtype")
    by_desc = DefaultQueryParams(
        "simple or extended (extended cost more credits)"
    )

    assert by_wire is by_desc


def test_bind_request_aliasing_uses_get_params_to_resolve_both_names():
    """bind_request's wire/python-name aliasing comes from get_params() shape.

    The dict maps python attr name (key) -> wire name (value), so it can be
    used to look up the wire form from either side: kwarg matches a key
    (python name) OR matches a value (wire name).
    """
    params = _DemoParams.get_params()
    python_names = set(params.keys())
    wire_names = set(params.values())

    assert "search_query" in python_names
    assert "search_query" in wire_names
    assert "msg_type" in python_names
    assert "msgtype" in wire_names
