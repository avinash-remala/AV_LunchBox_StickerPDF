"""
Tests for the marker logic module.
"""

import pytest
from av_lunchbox_stickerpdf.core.markers import get_marker_for_box_rice


class TestMarkerLogic:
    """Tests for get_marker_for_box_rice()."""

    # --- Comfort Box markers ---

    def test_veg_comfort_pulav(self):
        marker, size = get_marker_for_box_rice("Veg Comfort Box", "Pulav Rice")
        assert marker == "--- VP ---"
        assert size == 2

    def test_non_veg_comfort_pulav(self):
        marker, size = get_marker_for_box_rice("Non-Veg Comfort Box", "Pulav Rice")
        assert marker == "--- NVP ---"
        assert size == 2

    def test_veg_comfort_white(self):
        marker, size = get_marker_for_box_rice("Veg Comfort Box", "White Rice")
        assert marker == "--- VW ---"
        assert size == 2

    def test_non_veg_comfort_white(self):
        marker, size = get_marker_for_box_rice("Non-Veg Comfort Box", "White Rice")
        assert marker == "--- NVW ---"
        assert size == 2

    # --- Special Box markers ---

    def test_veg_special_box(self):
        marker, size = get_marker_for_box_rice("Veg Special Box", "Pulav Rice")
        assert marker == "--- VSP ---"
        assert size == 2

    def test_non_veg_special_box(self):
        marker, size = get_marker_for_box_rice("Non-Veg Special Box", "Pulav Rice")
        assert marker == "--- NVSP ---"
        assert size == 2

    def test_special_box_ignores_rice_type(self):
        """Special box marker should be the same regardless of rice type."""
        marker_pulav, _ = get_marker_for_box_rice("Non-Veg Special Box", "Pulav Rice")
        marker_white, _ = get_marker_for_box_rice("Non-Veg Special Box", "White Rice")
        assert marker_pulav == marker_white == "--- NVSP ---"

    # --- Edge cases ---

    def test_unknown_box_type_returns_empty(self):
        marker, size = get_marker_for_box_rice("Rajma Box", "White Rice")
        assert marker == ""
        assert size == 0

    def test_empty_strings(self):
        marker, size = get_marker_for_box_rice("", "")
        assert marker == ""
        assert size == 0

    def test_kabuli_chana_box(self):
        marker, size = get_marker_for_box_rice("Kabuli Chana Box", "Pulav Rice")
        assert marker == ""
        assert size == 0

    def test_non_veg_matched_before_veg(self):
        """Ensure 'Non-Veg' is not accidentally matched as 'Veg'."""
        marker, _ = get_marker_for_box_rice("Non-Veg Comfort Box", "Pulav Rice")
        assert marker == "--- NVP ---"
        assert "NV" in marker

    @pytest.mark.parametrize(
        "box_type, rice_type, expected_marker",
        [
            ("Veg Comfort Box", "Pulav Rice", "--- VP ---"),
            ("Non-Veg Comfort Box", "Pulav Rice", "--- NVP ---"),
            ("Veg Comfort Box", "White Rice", "--- VW ---"),
            ("Non-Veg Comfort Box", "White Rice", "--- NVW ---"),
            ("Veg Special Box", "Pulav Rice", "--- VSP ---"),
            ("Non-Veg Special Box", "White Rice", "--- NVSP ---"),
            ("Rajma Box", "White Rice", ""),
            ("Moong Dal Box", "Pulav Rice", ""),
            ("Unknown", "Unknown", ""),
        ],
    )
    def test_all_combinations(self, box_type, rice_type, expected_marker):
        marker, _ = get_marker_for_box_rice(box_type, rice_type)
        assert marker == expected_marker
