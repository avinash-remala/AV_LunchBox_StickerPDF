"""
Watermark utility module.
Converts a logo image to a grayscale watermark with configurable opacity,
and provides functions to insert it behind text in DOCX table cells.
"""

from pathlib import Path
from typing import Optional, Tuple
import io

from PIL import Image, ImageEnhance

from ..config.logging_config import get_logger

log = get_logger("utils.watermark")

# Default watermark settings
DEFAULT_OPACITY = 0.20  # 20% visibility
DEFAULT_CELL_SIZE = (200, 80)  # fits inside cell (6.47cm × 2.54cm) at ~96 DPI


def create_watermark_image(
    logo_path: str,
    opacity: float = DEFAULT_OPACITY,
    cell_size: Tuple[int, int] = DEFAULT_CELL_SIZE,
    output_path: Optional[str] = None,
) -> Optional[str]:
    """
    Convert a logo image to a grayscale watermark with specified opacity.

    Args:
        logo_path: Path to the original logo image (PNG/JPG).
        opacity: Opacity level (0.0 = invisible, 1.0 = fully visible). Default 5%.
        cell_size: Target (width, height) in pixels to fit inside a cell.
        output_path: Where to save the watermark. If None, saves next to the logo.

    Returns:
        Path to the generated watermark image, or None on failure.
    """
    try:
        logo = Path(logo_path)
        if not logo.exists():
            log.error(f"Logo file not found: {logo_path}")
            return None

        log.info(f"Creating watermark from: {logo_path} (opacity={opacity*100:.0f}%)")

        # 1. Open and convert to RGBA
        img = Image.open(logo_path).convert("RGBA")

        # 2. Convert to grayscale (luminance)
        grayscale = img.convert("L")

        # 3. Build the alpha channel:
        #    - Start with the original alpha (handles transparent logos)
        #    - Scale by the desired opacity
        orig_alpha = img.split()[3]
        # Multiply original alpha by opacity factor
        alpha = orig_alpha.point(lambda p: max(1, int(p * opacity)) if p > 10 else 0)

        # 4. Build final RGBA: all channels are gray, alpha controls visibility
        gray_rgba = Image.merge("RGBA", (
            grayscale,
            grayscale,
            grayscale,
            alpha,
        ))

        # 5. Resize to fit cell, maintaining aspect ratio
        gray_rgba.thumbnail(cell_size, Image.LANCZOS)

        # 6. Save directly (no canvas — avoids compositing that destroys alpha)
        if output_path is None:
            output_path = str(logo.parent / f"{logo.stem}_watermark.png")

        gray_rgba.save(output_path, "PNG")
        log.info(f"✓ Watermark saved: {output_path} ({gray_rgba.width}x{gray_rgba.height}px)")
        return output_path

    except Exception as e:
        log.error(f"Error creating watermark: {e}")
        return None


def get_watermark_bytes(watermark_path: str) -> Optional[io.BytesIO]:
    """
    Read a watermark image and return it as a BytesIO stream.
    Needed by python-docx for inline image insertion.

    Args:
        watermark_path: Path to the watermark PNG file.

    Returns:
        BytesIO stream of the image, or None on failure.
    """
    try:
        wm_path = Path(watermark_path)
        if not wm_path.exists():
            log.warning(f"Watermark file not found: {watermark_path}")
            return None

        buf = io.BytesIO(wm_path.read_bytes())
        buf.seek(0)
        return buf
    except Exception as e:
        log.error(f"Error reading watermark: {e}")
        return None


def get_default_watermark_path() -> Path:
    """Return the default path for the processed watermark image."""
    return Path(__file__).parent.parent.parent / "assets" / "logo_watermark.png"


def get_default_logo_path() -> Path:
    """Return the default path for the original logo image."""
    return Path(__file__).parent.parent.parent / "assets" / "logo.png"


def ensure_watermark(
    logo_path: Optional[str] = None,
    opacity: float = DEFAULT_OPACITY,
    cell_size: Tuple[int, int] = DEFAULT_CELL_SIZE,
) -> Optional[str]:
    """
    Ensure a watermark image exists. If not, create it from the logo.

    Args:
        logo_path: Path to logo. If None, uses default `assets/logo.png`.
        opacity: Opacity level (default 5%).
        cell_size: Target cell size in pixels.

    Returns:
        Path to the watermark image, or None if logo not available.
    """
    watermark_path = get_default_watermark_path()

    # If watermark already exists, reuse it
    if watermark_path.exists():
        log.debug(f"Using existing watermark: {watermark_path}")
        return str(watermark_path)

    # Otherwise, create from logo
    if logo_path is None:
        logo_path = str(get_default_logo_path())

    if not Path(logo_path).exists():
        log.warning(
            f"Logo not found at {logo_path}. "
            "Place your logo at assets/logo.png to enable watermarks."
        )
        return None

    return create_watermark_image(
        logo_path,
        opacity=opacity,
        cell_size=cell_size,
        output_path=str(watermark_path),
    )
