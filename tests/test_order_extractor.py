"""
Tests for the OrderExtractor from sheets_handler.
"""

import pytest
from av_lunchbox_stickerpdf.data.sheets_handler import OrderExtractor


class TestOrderExtractor:
    """Tests for OrderExtractor.extract_orders_from_rows()."""

    def setup_method(self):
        self.extractor = OrderExtractor()

    def test_extract_valid_rows(self):
        rows = [
            {"Full Name": "Abhishek Kumar", "Address": "2900 Plano Pkwy",
             "Type of Food": "Veg Comfort Box", "Type of Rice": "Pulav Rice"},
            {"Full Name": "Raj Patel", "Address": "3400 W Plano Pkwy",
             "Type of Food": "Non-Veg Comfort Box", "Type of Rice": "White Rice"},
        ]
        orders = self.extractor.extract_orders_from_rows(rows)
        assert len(orders) == 2
        assert orders[0].name == "Abhishek Kumar"
        assert orders[1].box_type == "Non-Veg Comfort Box"

    def test_skip_empty_name_rows(self):
        rows = [
            {"Full Name": "", "Address": "2900 Plano Pkwy",
             "Type of Food": "Veg Comfort Box", "Type of Rice": "Pulav Rice"},
            {"Full Name": "Valid User", "Address": "2900 Plano Pkwy",
             "Type of Food": "Veg Comfort Box", "Type of Rice": "Pulav Rice"},
        ]
        orders = self.extractor.extract_orders_from_rows(rows)
        assert len(orders) == 1
        assert orders[0].name == "Valid User"

    def test_skip_empty_address_rows(self):
        rows = [
            {"Full Name": "No Address", "Address": "",
             "Type of Food": "Veg Comfort Box", "Type of Rice": "Pulav Rice"},
        ]
        orders = self.extractor.extract_orders_from_rows(rows)
        assert len(orders) == 0

    def test_empty_rows_list(self):
        orders = self.extractor.extract_orders_from_rows([])
        assert orders == []

    def test_custom_column_mapping(self):
        extractor = OrderExtractor(column_mapping={
            "name": "Customer",
            "address": "Location",
            "box_type": "Box",
            "rice_type": "Rice",
        })
        rows = [
            {"Customer": "Jane Doe", "Location": "123 Main St",
             "Box": "Rajma Box", "Rice": "White Rice"},
        ]
        orders = extractor.extract_orders_from_rows(rows)
        assert len(orders) == 1
        assert orders[0].name == "Jane Doe"
        assert orders[0].box_type == "Rajma Box"

    def test_whitespace_stripped(self):
        rows = [
            {"Full Name": "  Padded Name  ", "Address": "  2900 Plano Pkwy  ",
             "Type of Food": " Veg Comfort Box ", "Type of Rice": " Pulav Rice "},
        ]
        orders = self.extractor.extract_orders_from_rows(rows)
        assert orders[0].name == "Padded Name"
        assert orders[0].rice_type == "Pulav Rice"

    def test_order_ids_assigned(self):
        rows = [
            {"Full Name": "User A", "Address": "Addr A",
             "Type of Food": "Veg Comfort Box", "Type of Rice": "Pulav Rice"},
            {"Full Name": "User B", "Address": "Addr B",
             "Type of Food": "Non-Veg Comfort Box", "Type of Rice": "White Rice"},
        ]
        orders = self.extractor.extract_orders_from_rows(rows)
        assert orders[0].order_id == 0
        assert orders[1].order_id == 1
