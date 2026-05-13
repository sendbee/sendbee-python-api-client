"""Tests for Field subclasses: type coercion and fallback behavior."""

from datetime import datetime

import pytest

from sendbee_api.fields import (
    Field,
    NumberField,
    RealNumberField,
    TextField,
    BooleanField,
    DatetimeField,
    ListField,
    ModelField,
)
from sendbee_api.models import Model


class _StubModel:
    """Minimal stand-in that exposes the only attribute Field reads."""
    def __init__(self, item):
        self.item = item


def _convert(field, item_dict):
    field.convert_item(_StubModel(item_dict))
    return field.value


def test_number_field_converts_numeric_string_to_int():
    """Numeric strings parse to int."""
    assert _convert(NumberField(index="n"), {"n": "42"}) == 42


def test_number_field_returns_zero_for_non_numeric_string():
    """Non-numeric input falls back to 0, not exception."""
    assert _convert(NumberField(index="n"), {"n": "abc"}) == 0


def test_real_number_field_converts_decimal_string_to_float():
    """Decimal strings parse to float."""
    assert _convert(RealNumberField(index="x"), {"x": "3.14"}) == 3.14


def test_real_number_field_returns_zero_point_zero_for_invalid_input():
    """Non-numeric input falls back to 0.0."""
    assert _convert(RealNumberField(index="x"), {"x": "abc"}) == 0.0


def test_text_field_coerces_int_to_string():
    """Integer values are stringified."""
    assert _convert(TextField(index="t"), {"t": 7}) == "7"


def test_boolean_field_coerces_truthy_to_true():
    """Non-empty string is truthy."""
    assert _convert(BooleanField(index="b"), {"b": "yes"}) is True


def test_boolean_field_coerces_zero_to_false():
    """0 is falsy."""
    assert _convert(BooleanField(index="b"), {"b": 0}) is False


def test_datetime_field_parses_with_provided_format():
    """Provided strftime format parses an ISO-style timestamp."""
    field = DatetimeField(index="ts", format="%Y-%m-%d %H:%M:%S")

    value = _convert(field, {"ts": "2024-01-02 03:04:05"})

    assert value == datetime(2024, 1, 2, 3, 4, 5)


def test_datetime_field_returns_raw_string_when_format_mismatches():
    """A value that doesn't match the format is returned unchanged (no raise)."""
    field = DatetimeField(index="ts", format="%Y-%m-%d %H:%M:%S")

    assert _convert(field, {"ts": "not-a-date"}) == "not-a-date"


def test_list_field_passes_list_values_through():
    """A list input is preserved."""
    assert _convert(ListField(index="l"), {"l": ["a", "b"]}) == ["a", "b"]


def test_field_returns_none_when_index_missing_from_item():
    """Missing key on the item dict yields None, not KeyError."""
    assert _convert(TextField(index="missing"), {"other": "x"}) is None


def test_field_returns_none_when_value_is_none():
    """Explicit None passes through as None."""
    assert _convert(TextField(index="t"), {"t": None}) is None


def test_model_field_stores_target_model_class():
    """ModelField records the nested model class for later recursion."""
    class Inner(Model):
        pass

    field = ModelField(Inner, index="nested")

    assert field.model_cls is Inner
    assert field.index == "nested"
