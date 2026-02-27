"""
Tests for core data models.
"""

import pytest
from datetime import datetime
from av_lunchbox_stickerpdf.core.models import Order, BoxType, RiceType, Summary


class TestBoxType:
    """Tests for the BoxType enum."""

    def test_standard_box_types(self):
        assert BoxType.VEG_COMFORT == "Veg Comfort Box"
        assert BoxType.NON_VEG_COMFORT == "Non-Veg Comfort Box"
        assert BoxType.VEG_SPECIAL == "Veg Special Box"
        assert BoxType.NON_VEG_SPECIAL == "Non-Veg Special Box"
        assert BoxType.KABULI_CHANA == "Kabuli Chana Box"
        assert BoxType.MOONG_DAL == "Moong Dal Box"
        assert BoxType.RAJMA == "Rajma Box"
        assert BoxType.UNKNOWN == "Unknown"

    def test_box_type_is_string(self):
        assert isinstance(BoxType.VEG_COMFORT, str)
        assert "Comfort" in BoxType.VEG_COMFORT


class TestRiceType:
    """Tests for the RiceType enum."""

    def test_rice_types(self):
        assert RiceType.PULAV == "Pulav Rice"
        assert RiceType.WHITE == "White Rice"
        assert RiceType.UNKNOWN == "Unknown"


class TestOrder:
    """Tests for the Order dataclass."""

    def test_create_order(self):
        order = Order(
            name="Abhishek Kumar",
            address="2900 Plano Pkwy",
            box_type="Veg Comfort Box",
            rice_type="Pulav Rice",
        )
        assert order.name == "Abhishek Kumar"
        assert order.address == "2900 Plano Pkwy"
        assert order.box_type == "Veg Comfort Box"
        assert order.rice_type == "Pulav Rice"
        assert order.order_id is None
        assert order.metadata == {}

    def test_order_strips_whitespace(self):
        order = Order(
            name="  Raj Patel  ",
            address="  3400 W Plano Pkwy  ",
            box_type="  Non-Veg Comfort Box  ",
            rice_type="  White Rice  ",
        )
        assert order.name == "Raj Patel"
        assert order.address == "3400 W Plano Pkwy"
        assert order.box_type == "Non-Veg Comfort Box"
        assert order.rice_type == "White Rice"

    def test_order_handles_empty_strings(self):
        order = Order(name="", address="", box_type="", rice_type="")
        assert order.name == ""
        assert order.metadata == {}

    def test_order_handles_none_strings(self):
        order = Order(name=None, address=None, box_type=None, rice_type=None)
        assert order.name == ""
        assert order.address == ""

    def test_order_to_dict(self):
        order = Order(
            name="Test User",
            address="123 Main St",
            box_type="Veg Comfort Box",
            rice_type="Pulav Rice",
            order_id=1,
        )
        d = order.to_dict()
        assert d["name"] == "Test User"
        assert d["order_id"] == 1
        assert d["timestamp"] is None

    def test_order_from_dict(self):
        data = {
            "name": "Test User",
            "address": "123 Main St",
            "box_type": "Non-Veg Comfort Box",
            "rice_type": "White Rice",
            "order_id": 5,
        }
        order = Order.from_dict(data)
        assert order.name == "Test User"
        assert order.order_id == 5
        assert order.rice_type == "White Rice"

    def test_order_roundtrip(self):
        original = Order(
            name="Round Trip",
            address="456 Oak Ave",
            box_type="Rajma Box",
            rice_type="Pulav Rice",
            order_id=10,
        )
        rebuilt = Order.from_dict(original.to_dict())
        assert rebuilt.name == original.name
        assert rebuilt.box_type == original.box_type
        assert rebuilt.order_id == original.order_id


class TestSummary:
    """Tests for the Summary dataclass."""

    def test_create_summary(self):
        summary = Summary(
            total_boxes=10,
            box_combinations={"Veg Comfort Box + Pulav Rice": 5},
            address_counts={"2900 Plano Pkwy": 7},
            generated_at=datetime(2026, 2, 20, 12, 0),
        )
        assert summary.total_boxes == 10
        assert summary.date_for is None

    def test_summary_to_dict(self):
        summary = Summary(
            total_boxes=3,
            box_combinations={"Veg Comfort Box + Pulav Rice": 3},
            address_counts={"2900 Plano Pkwy": 3},
            generated_at=datetime(2026, 2, 20, 12, 0),
            date_for="2026-02-20",
        )
        d = summary.to_dict()
        assert d["total_boxes"] == 3
        assert d["date_for"] == "2026-02-20"
        assert "2026-02-20" in d["generated_at"]
