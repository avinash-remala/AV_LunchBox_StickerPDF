#!/usr/bin/env python3
"""
Test script to verify Google Sheets integration
"""

from sheets_handler import get_todays_lunch_orders
from datetime import datetime

SPREADSHEET_ID = "1442BcVZmlIU9nHhpoHi5to95AAWwU5VYjPMEUHg8azI"

print(f"Testing Google Sheets integration for {datetime.now().strftime('%Y-%m-%d')}")
print("=" * 60)

orders = get_todays_lunch_orders(SPREADSHEET_ID)

if orders:
    print(f"\n✓ Successfully retrieved {len(orders)} order(s) for today:\n")
    for i, order in enumerate(orders, 1):
        print(f"Order {i}:")
        print(f"  Name: {order['name']}")
        print(f"  Address: {order['address']}")
        print(f"  Box Type: {order['box_type']}")
        print(f"  Rice Type: {order['rice_type']}")
        print()
else:
    print("\n✗ No orders found for today")
    print("\nMake sure:")
    print("1. The sheet contains a 'Date' column with today's date (MM/DD/YYYY)")
    print("2. The sheet has columns: Name, Address, Box Type, Rice Type")
    print("3. The Google Sheet is public (or you have access)")

print("=" * 60)
