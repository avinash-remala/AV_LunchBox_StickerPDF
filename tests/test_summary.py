"""
Tests for the summary generation module.
"""

import pytest
from av_lunchbox_stickerpdf.core.models import Order
from av_lunchbox_stickerpdf.report.summary_generator import SummaryGenerator, SummaryWriter


def _make_order(name="Test User", address="2900 Plano Pkwy",
                box_type="Veg Comfort Box", rice_type="Pulav Rice"):
    """Helper to create an Order quickly."""
    return Order(name=name, address=address, box_type=box_type, rice_type=rice_type)


class TestSummaryGenerator:
    """Tests for SummaryGenerator.generate()."""

    def test_empty_orders(self):
        result = SummaryGenerator.generate([])
        assert "No orders found" in result

    def test_single_order(self):
        orders = [_make_order()]
        result = SummaryGenerator.generate(orders)
        assert "TOTAL BOXES: 1" in result
        assert "Veg Comfort Box + Pulav Rice: 1" in result

    def test_multiple_orders(self):
        orders = [
            _make_order(box_type="Veg Comfort Box", rice_type="Pulav Rice"),
            _make_order(box_type="Veg Comfort Box", rice_type="Pulav Rice"),
            _make_order(box_type="Non-Veg Comfort Box", rice_type="White Rice"),
        ]
        result = SummaryGenerator.generate(orders)
        assert "TOTAL BOXES: 3" in result
        assert "Veg Comfort Box + Pulav Rice: 2" in result
        assert "Non-Veg Comfort Box + White Rice: 1" in result

    def test_address_counts(self):
        orders = [
            _make_order(address="2900 Plano Pkwy"),
            _make_order(address="2900 Plano Pkwy"),
            _make_order(address="3400 W Plano Pkwy"),
        ]
        result = SummaryGenerator.generate(orders)
        assert "2900 Plano Pkwy: 2 boxes" in result
        assert "3400 W Plano Pkwy: 1 box" in result

    def test_special_box_in_summary(self):
        orders = [
            _make_order(box_type="Veg Special Box", rice_type="Pulav Rice"),
            _make_order(box_type="Non-Veg Special Box", rice_type="White Rice"),
        ]
        result = SummaryGenerator.generate(orders)
        assert "TOTAL BOXES: 2" in result
        assert "Veg Special Box + Pulav Rice: 1" in result
        assert "Non-Veg Special Box + White Rice: 1" in result

    def test_non_standard_combination(self):
        orders = [_make_order(box_type="Rajma Box", rice_type="White Rice")]
        result = SummaryGenerator.generate(orders)
        assert "Rajma Box + White Rice: 1" in result

    def test_zero_counts_for_unused_combos(self):
        orders = [_make_order(box_type="Veg Comfort Box", rice_type="Pulav Rice")]
        result = SummaryGenerator.generate(orders)
        assert "Non-Veg Comfort Box + Pulav Rice: 0" in result
        assert "Veg Comfort Box + White Rice: 0" in result


class TestSummaryGeneratorObject:
    """Tests for SummaryGenerator.generate_summary_object()."""

    def test_summary_object(self):
        orders = [
            _make_order(box_type="Veg Comfort Box", rice_type="Pulav Rice"),
            _make_order(box_type="Non-Veg Comfort Box", rice_type="White Rice"),
        ]
        summary = SummaryGenerator.generate_summary_object(orders, date_for="2026-02-20")
        assert summary.total_boxes == 2
        assert summary.date_for == "2026-02-20"
        assert summary.box_combinations["Veg Comfort Box + Pulav Rice"] == 1


class TestSummaryWriter:
    """Tests for SummaryWriter.save_summary()."""

    def test_save_summary_creates_file(self, tmp_path):
        text = "TOTAL BOXES: 5"
        result = SummaryWriter.save_summary(text, str(tmp_path), "test_summary.txt")
        assert result is not None
        assert (tmp_path / "test_summary.txt").exists()
        assert (tmp_path / "test_summary.txt").read_text() == text

    def test_save_summary_auto_filename(self, tmp_path):
        text = "TOTAL BOXES: 3"
        result = SummaryWriter.save_summary(text, str(tmp_path))
        assert result is not None
        # File should exist and contain the text
        from pathlib import Path
        saved = Path(result)
        assert saved.exists()
        assert saved.read_text() == text

    def test_save_summary_from_orders(self, tmp_path):
        orders = [_make_order(), _make_order()]
        result = SummaryWriter.save_summary_from_orders(orders, str(tmp_path), "orders.txt")
        assert result is not None
        from pathlib import Path
        content = Path(result).read_text()
        assert "TOTAL BOXES: 2" in content
