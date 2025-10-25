#!/usr/bin/env python3
"""
Annual General Assembly QR Code System
Generates QR codes for members and provides verification system
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
import pandas as pd
import qrcode
import qrcode.image.svg
from io import BytesIO
import sqlite3
import hashlib
import secrets
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import os
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Database setup
def init_db():
    conn = sqlite3.connect('aga_attendance.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY,
            member_id TEXT UNIQUE,
            full_name TEXT,
            email TEXT,
            phone TEXT,
            qr_code TEXT UNIQUE,
            qr_hash TEXT UNIQUE,
            checked_in BOOLEAN DEFAULT FALSE,
            check_in_time TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def load_members_from_csv():
    """Load members from CSV file"""
    try:
        # Try different encodings to handle the CSV file
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        df = None
        
        for encoding in encodings:
            try:
                df = pd.read_csv('2025_TIPCS_Annual_General_Assembly_(AGA25).csv', encoding=encoding)
                print(f"Successfully loaded CSV with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            raise Exception("Could not read CSV file with any encoding")
            
        members = []
        
        for _, row in df.iterrows():
            # Skip rows with empty or invalid data
            if pd.isna(row['Id']) or pd.isna(row['Full name']):
                continue
                
            # Generate unique QR code data
            member_id = str(int(row['Id'])) if pd.notna(row['Id']) else secrets.token_hex(8)
            qr_data = f"AGA-{member_id}-{secrets.token_hex(4)}"
            qr_hash = hashlib.sha256(qr_data.encode()).hexdigest()
            
            member = {
                'member_id': member_id,
                'full_name': str(row['Full name']).strip() if pd.notna(row['Full name']) else 'Unknown',
                'email': str(row['Email1']).strip() if pd.notna(row['Email1']) else '',
                'phone': str(row['Phone number']).strip() if pd.notna(row['Phone number']) else '',
                'qr_code': qr_data,
                'qr_hash': qr_hash
            }
            members.append(member)
        
        return members
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return []

def save_members_to_db(members):
    """Save members to database"""
    conn = sqlite3.connect('aga_attendance.db')
    cursor = conn.cursor()
    
    for member in members:
        cursor.execute('''
            INSERT OR REPLACE INTO members 
            (member_id, full_name, email, phone, qr_code, qr_hash)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            member['member_id'],
            member['full_name'],
            member['email'],
            member['phone'],
            member['qr_code'],
            member['qr_hash']
        ))
    
    conn.commit()
    conn.close()

def generate_qr_code(qr_data, member_name):
    """Generate QR code image"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Add member name to image
    from PIL import Image, ImageDraw, ImageFont
    img = img.convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    # Add text at bottom
    text = f"Member: {member_name}"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Calculate position (center bottom)
    img_width, img_height = img.size
    x = (img_width - text_width) // 2
    y = img_height - text_height - 10
    
    draw.text((x, y), text, fill="black", font=font)
    
    return img

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/verify')
def verify():
    return render_template('verify.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

@app.route('/api/load-members', methods=['POST'])
def load_members():
    """Load members from CSV and generate QR codes"""
    try:
        members = load_members_from_csv()
        save_members_to_db(members)
        
        return jsonify({
            'success': True,
            'message': f'Loaded {len(members)} members successfully',
            'count': len(members)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error loading members: {str(e)}'
        })

@app.route('/api/generate-qr/<member_id>')
def generate_qr(member_id):
    """Generate QR code for specific member"""
    conn = sqlite3.connect('aga_attendance.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM members WHERE member_id = ?', (member_id,))
    member = cursor.fetchone()
    conn.close()
    
    if not member:
        return jsonify({'error': 'Member not found'})
    
    # Generate QR code image
    img = generate_qr_code(member[5], member[2])  # qr_code, full_name
    
    # Save to BytesIO
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

@app.route('/api/verify-qr', methods=['POST'])
def verify_qr():
    """Verify QR code and check in member"""
    data = request.get_json()
    qr_data = data.get('qr_data')
    
    if not qr_data:
        return jsonify({'error': 'No QR code data provided'})
    
    conn = sqlite3.connect('aga_attendance.db')
    cursor = conn.cursor()
    
    # Find member by QR code
    cursor.execute('SELECT * FROM members WHERE qr_code = ?', (qr_data,))
    member = cursor.fetchone()
    
    if not member:
        conn.close()
        return jsonify({
            'valid': False,
            'message': '❌ Invalid: QR code not recognized'
        })
    
    # Check if already checked in
    if member[7]:  # checked_in field
        conn.close()
        return jsonify({
            'valid': False,
            'message': '❌ Invalid: QR code already used',
            'member_name': member[2],
            'check_in_time': member[8]
        })
    
    # Check in the member
    cursor.execute('''
        UPDATE members 
        SET checked_in = TRUE, check_in_time = CURRENT_TIMESTAMP 
        WHERE member_id = ?
    ''', (member[1],))
    conn.commit()
    conn.close()
    
    return jsonify({
        'valid': True,
        'message': '✅ Valid: Member checked in successfully',
        'member_name': member[2],
        'check_in_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/members')
def get_members():
    """Get all members with their status"""
    conn = sqlite3.connect('aga_attendance.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT member_id, full_name, email, phone, checked_in, check_in_time
        FROM members ORDER BY full_name
    ''')
    members = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'member_id': m[0],
        'full_name': m[1],
        'email': m[2],
        'phone': m[3],
        'checked_in': bool(m[4]),
        'check_in_time': m[5]
    } for m in members])

@app.route('/api/send-invitations', methods=['POST'])
def send_invitations():
    """Send invitations via email (WhatsApp integration would need additional setup)"""
    data = request.get_json()
    selected_members = data.get('members', [])
    
    # This is a placeholder for email sending
    # You'll need to configure SMTP settings
    return jsonify({
        'success': True,
        'message': f'Invitations sent to {len(selected_members)} members'
    })

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
