"""
Marker logic for box/rice type combinations.
Determines the visual marker printed on sticker labels.
"""

from typing import Tuple


# Marker definitions: (marker_string, font_size_increase_pt)
MARKERS = {
    ("Veg", "Comfort Box", "Pulav Rice"):       ("--- VP ---", 2),
    ("Non-Veg", "Comfort Box", "Pulav Rice"):    ("--- NVP ---", 2),
    ("Veg", "Comfort Box", "White Rice"):        ("--- VW ---", 2),
    ("Non-Veg", "Comfort Box", "White Rice"):    ("--- NVW ---", 2),
    ("Non-Veg", "Special Box", None):            ("--- NVSP ---", 2),
    ("Veg", "Special Box", None):                ("--- VSP ---", 2),
}


def get_marker_for_box_rice(box_type: str, rice_type: str) -> Tuple[str, int]:
    """
    Determine the marker and font size increase based on box and rice type.

    Args:
        box_type: The box type string (e.g., "Veg Comfort Box", "Non-Veg Special Box")
        rice_type: The rice type string (e.g., "Pulav Rice", "White Rice")

    Returns:
        Tuple of (marker_string, font_size_increase_pt).
        Returns ("", 0) if no marker matches.

    Examples:
        >>> get_marker_for_box_rice("Veg Comfort Box", "Pulav Rice")
        ('--- VP ---', 2)
        >>> get_marker_for_box_rice("Non-Veg Special Box", "White Rice")
        ('--- NVSP ---', 2)
        >>> get_marker_for_box_rice("Rajma Box", "White Rice")
        ('', 0)
    """
    # Determine veg/non-veg (check Non-Veg first to avoid false match on "Veg")
    is_non_veg = "Non-Veg" in box_type
    is_veg = "Veg" in box_type and not is_non_veg
    veg_key = "Non-Veg" if is_non_veg else ("Veg" if is_veg else None)

    if veg_key is None:
        return "", 0

    # Determine box category
    is_special_box = "Special Box" in box_type
    is_comfort_box = "Comfort Box" in box_type

    # Special Box — rice type doesn't matter
    if is_special_box:
        result = MARKERS.get((veg_key, "Special Box", None))
        if result:
            return result

    # Comfort Box — rice type matters
    if is_comfort_box:
        is_pulav = "Pulav Rice" in rice_type
        rice_key = "Pulav Rice" if is_pulav else "White Rice"
        result = MARKERS.get((veg_key, "Comfort Box", rice_key))
        if result:
            return result

    return "", 0
