"""
Summary report generation module.
Creates formatted text reports from order data.
"""

from datetime import datetime
from pathlib import Path
from collections import defaultdict, Counter
from typing import List, Optional, Dict, Any

from ..core.models import Order, Summary


class SummaryGenerator:
    """Generates summary reports from order data."""
    
    STANDARD_COMBINATIONS = [
        "Veg Comfort Box + Pulav Rice",
        "Non-Veg Comfort Box + Pulav Rice",
        "Veg Comfort Box + White Rice",
        "Non-Veg Comfort Box + White Rice",
        "Veg Special Box + Pulav Rice",
        "Veg Special Box + White Rice",
        "Non-Veg Special Box + Pulav Rice",
        "Non-Veg Special Box + White Rice",
    ]
    
    @classmethod
    def generate(cls, orders: List[Order]) -> str:
        """
        Generate a summary report from a list of orders.
        
        Args:
            orders: List of Order objects
        
        Returns:
            String containing the formatted summary
        """
        
        if not orders:
            return "No orders found for this date."
        
        # Count total boxes
        total_boxes = len(orders)
        
        # Count by box type + rice type combination
        box_rice_combinations = Counter()
        for order in orders:
            combination = f"{order.box_type} + {order.rice_type}"
            box_rice_combinations[combination] += 1
        
        # Count by address
        address_counts = defaultdict(int)
        for order in orders:
            address_counts[order.address] += 1
        
        # Build summary text
        summary_lines = []
        summary_lines.append(f"TOTAL BOXES: {total_boxes}\n")
        
        # Box types section
        summary_lines.append("Boxes (count by type)")
        
        # Add all standard combinations (with counts or 0)
        for combo in cls.STANDARD_COMBINATIONS:
            count = box_rice_combinations.get(combo, 0)
            summary_lines.append(f"•\t{combo}: {count}")
        
        # Add any non-standard combinations
        for combo, count in sorted(box_rice_combinations.items()):
            if combo not in cls.STANDARD_COMBINATIONS:
                summary_lines.append(f"•\t{combo}: {count}")
        
        # Addresses section
        summary_lines.append("\nAddresses (total boxes per address)")
        
        # Sort addresses for consistency
        for address in sorted(address_counts.keys()):
            count = address_counts[address]
            box_word = "box" if count == 1 else "boxes"
            summary_lines.append(f"•\t{address}: {count} {box_word}")
        
        return "\n".join(summary_lines)
    
    @classmethod
    def generate_summary_object(cls, orders: List[Order], date_for: Optional[str] = None) -> Summary:
        """
        Generate a Summary object from orders.
        
        Args:
            orders: List of Order objects
            date_for: Optional date string for the summary
        
        Returns:
            Summary object
        """
        total_boxes = len(orders)
        
        box_combinations = {}
        for combo in cls.STANDARD_COMBINATIONS:
            box_combinations[combo] = sum(
                1 for order in orders
                if f"{order.box_type} + {order.rice_type}" == combo
            )
        
        # Add non-standard combinations
        for order in orders:
            combo = f"{order.box_type} + {order.rice_type}"
            if combo not in cls.STANDARD_COMBINATIONS:
                box_combinations[combo] = box_combinations.get(combo, 0) + 1
        
        address_counts = {}
        for order in orders:
            address_counts[order.address] = address_counts.get(order.address, 0) + 1
        
        return Summary(
            total_boxes=total_boxes,
            box_combinations=box_combinations,
            address_counts=address_counts,
            generated_at=datetime.now(),
            date_for=date_for,
        )


class SummaryWriter:
    """Writes summary reports to files."""
    
    @staticmethod
    def save_summary(summary_text: str, output_dir: str = "exports", filename: Optional[str] = None) -> Optional[str]:
        """
        Save summary text to a file.
        
        Args:
            summary_text: The summary text to save
            output_dir: Directory to save the summary file
            filename: Optional custom filename. If not provided, uses timestamp.
        
        Returns:
            Path to the saved file, or None if save failed
        """
        
        # Create output directory if it doesn't exist
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Determine filename
        if filename is None:
            # Generate filename with timestamp: YYYY-MM-DD_HH:MM AM/PM.txt
            now = datetime.now()
            filename = now.strftime("%Y-%m-%d_%I:%M %p.txt")
        
        # Handle if filename is a full path vs just filename
        if "/" in filename or "\\" in filename:
            full_path = Path(filename)
        else:
            full_path = output_path / filename
        
        # Ensure parent directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(full_path, 'w') as f:
                f.write(summary_text)
            
            print(f"✓ Summary saved to: {full_path}")
            return str(full_path)
        
        except Exception as e:
            print(f"✗ Error saving summary: {e}")
            return None
    
    @staticmethod
    def save_summary_from_orders(orders: List[Order], output_dir: str = "exports", 
                                  filename: Optional[str] = None) -> Optional[str]:
        """
        Generate and save summary from orders.
        
        Args:
            orders: List of Order objects
            output_dir: Directory to save the summary
            filename: Optional custom filename
        
        Returns:
            Path to the saved file, or None if save failed
        """
        summary_text = SummaryGenerator.generate(orders)
        return SummaryWriter.save_summary(summary_text, output_dir, filename)
