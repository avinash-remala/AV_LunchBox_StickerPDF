#!/usr/bin/env python3
"""
Generate summary reports from lunch box order data.
Creates a formatted text file with statistics about orders.
"""

from datetime import datetime
from pathlib import Path
from collections import defaultdict, Counter
import os


def generate_summary(orders):
    """
    Generate a summary report from a list of orders.
    
    Args:
        orders: List of order dictionaries with keys: name, address, box_type, rice_type
    
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
        box_type = order.get('box_type', 'Unknown').strip()
        rice_type = order.get('rice_type', 'Unknown').strip()
        combination = f"{box_type} + {rice_type}"
        box_rice_combinations[combination] += 1
    
    # Count by address
    address_counts = defaultdict(int)
    for order in orders:
        address = order.get('address', 'Unknown').strip()
        address_counts[address] += 1
    
    # Build summary text
    summary_lines = []
    summary_lines.append(f"TOTAL BOXES: {total_boxes}\n")
    
    # Box types section
    summary_lines.append("Boxes (count by type)")
    
    # Define the standard combinations we expect
    standard_combinations = [
        "Veg Comfort Box + Pulav Rice",
        "Non-Veg Comfort Box + Pulav Rice",
        "Veg Comfort Box + White Rice",
        "Non-Veg Comfort Box + White Rice"
    ]
    
    # Add all standard combinations (only those with non-zero counts)
    for combo in standard_combinations:
        count = box_rice_combinations.get(combo, 0)
        if count > 0:
            summary_lines.append(f"•\t{combo}: {count}")
    
    # Add any non-standard combinations
    for combo, count in sorted(box_rice_combinations.items()):
        if combo not in standard_combinations:
            summary_lines.append(f"•\t{combo}: {count}")
    
    # Addresses section
    summary_lines.append("\nAddresses (total boxes per address)")
    
    # Sort addresses for consistency
    for address in sorted(address_counts.keys()):
        count = address_counts[address]
        box_word = "box" if count == 1 else "boxes"
        summary_lines.append(f"•\t{address}: {count} {box_word}")
    
    return "\n".join(summary_lines)


def save_summary(orders, output_dir="exports", filename=None):
    """
    Generate summary and save to a text file.
    
    Args:
        orders: List of order dictionaries
        output_dir: Directory to save the summary file (default: exports).
                   Can be a string or Path object.
        filename: Optional custom filename. If not provided, uses timestamp.
                 Can be a full path or just filename.
    
    Returns:
        Path to the saved summary file, or None if save failed
    """
    
    # Convert to Path object if it's a string
    output_dir = str(output_dir)  # Ensure it's a string
    
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
        # Generate summary
        summary = generate_summary(orders)
        
        # Save to file
        with open(full_path, 'w') as f:
            f.write(summary)
        
        print(f"\n✓ Summary saved to: {full_path}")
        return str(full_path)
    
    except Exception as e:
        print(f"\n✗ Error saving summary: {e}")
        return None


def generate_and_save_summary(orders, output_dir="exports"):
    """
    Generate and save summary with auto-generated timestamp filename.
    
    Args:
        orders: List of order dictionaries
        output_dir: Directory to save the summary
    
    Returns:
        Path to the saved file
    """
    return save_summary(orders, output_dir)


if __name__ == "__main__":
    # Test with sample data
    sample_orders = [
        {'name': 'Abhishek Kumar', 'address': '2900 Plano Pkwy', 'box_type': 'Veg Comfort Box', 'rice_type': 'Pulav Rice'},
        {'name': 'Raj Patel', 'address': '2900 Plano Pkwy', 'box_type': 'Non-Veg Comfort Box', 'rice_type': 'Pulav Rice'},
        {'name': 'Priya Singh', 'address': '3400 W Plano Pkwy', 'box_type': 'Veg Comfort Box', 'rice_type': 'Pulav Rice'},
        {'name': 'John Doe', 'address': '2900 Plano Pkwy', 'box_type': 'Veg Comfort Box', 'rice_type': 'White Rice'},
        {'name': 'Jane Smith', 'address': '3400 W Plano Pkwy', 'box_type': 'Non-Veg Comfort Box', 'rice_type': 'White Rice'},
    ]
    
    print("Sample Summary:")
    print(generate_summary(sample_orders))
    print("\n" + "="*50 + "\n")
    
    # Test saving
    save_summary(sample_orders)
