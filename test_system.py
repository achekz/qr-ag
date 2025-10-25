#!/usr/bin/env python3
"""
Test script for AGA QR Code System
"""

import sqlite3
import pandas as pd
from app import load_members_from_csv, save_members_to_db, init_db

def test_system():
    print("Testing AGA QR Code System...")
    print("=" * 50)
    
    # Test 1: Initialize database
    print("1. Initializing database...")
    init_db()
    print("OK - Database initialized successfully")
    
    # Test 2: Load members from CSV
    print("\n2. Loading members from CSV...")
    members = load_members_from_csv()
    print(f"OK - Loaded {len(members)} members from CSV")
    
    if len(members) > 0:
        print(f"   First member: {members[0]['full_name']}")
        print(f"   Sample QR code: {members[0]['qr_code']}")
    
    # Test 3: Save members to database
    print("\n3. Saving members to database...")
    save_members_to_db(members)
    print("OK - Members saved to database successfully")
    
    # Test 4: Verify database contents
    print("\n4. Verifying database contents...")
    conn = sqlite3.connect('aga_attendance.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM members')
    count = cursor.fetchone()[0]
    print(f"OK - Database contains {count} members")
    
    cursor.execute('SELECT full_name, qr_code FROM members LIMIT 3')
    sample_members = cursor.fetchall()
    print("   Sample members:")
    for name, qr in sample_members:
        print(f"   - {name}: {qr}")
    
    conn.close()
    
    print("\n" + "=" * 50)
    print("OK - All tests passed! System is ready to use.")
    print("\nTo start the web application, run: python app.py")
    print("Then open your browser to: http://localhost:5000")

if __name__ == "__main__":
    test_system()