#!/usr/bin/env python3
"""
Annual General Assembly QR Code System
Generates QR codes for members and provides verification system
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
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
from functools import wraps

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Admin credentials
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admintipcs'

# Authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

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

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error='Invalid username or password')
    
    return render_template('login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('admin_login'))

@app.route('/admin')
@admin_required
def admin():
    return render_template('admin.html')

@app.route('/verify')
def verify():
    return render_template('verify.html')

@app.route('/mobile')
def mobile():
    return render_template('mobile.html')

@app.route('/api/load-members', methods=['POST'])
@admin_required
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

@app.route('/api/members-with-qr')
@admin_required
def get_members_with_qr():
    """Get all members with their QR codes for email sending"""
    conn = sqlite3.connect('aga_attendance.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT member_id, full_name, email, phone, qr_code, checked_in, check_in_time
        FROM members ORDER BY full_name
    ''')
    members = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'member_id': m[0],
        'full_name': m[1],
        'email': m[2],
        'phone': m[3],
        'qr_code': m[4],
        'checked_in': bool(m[5]),
        'check_in_time': m[6]
    } for m in members])

@app.route('/api/send-invitations', methods=['POST'])
@admin_required
def send_invitations():
    """Send invitations via email"""
    data = request.get_json()
    selected_members = data.get('members', [])
    send_type = data.get('type', 'bulk')  # 'bulk' or 'individual'
    
    if not selected_members:
        return jsonify({
            'success': False,
            'message': 'No members selected for sending invitations'
        })
    
    try:
        from email_service import EmailService
        email_service = EmailService()
        
        if send_type == 'individual':
            # Send to individual member
            member = selected_members[0]
            success, message = email_service.send_single_invitation(
                member['member_id'],
                member['full_name'],
                member['email'],
                member['qr_code']
            )
            
            return jsonify({
                'success': success,
                'message': message,
                'member': member['full_name']
            })
        else:
            # Send bulk invitations
            results = email_service.send_bulk_invitations(selected_members)
            stats = email_service.get_email_stats(results)
            
            return jsonify({
                'success': True,
                'message': f'Bulk email sending completed. {stats["successful"]}/{stats["total"]} emails sent successfully.',
                'stats': stats,
                'results': results
            })
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error sending invitations: {str(e)}'
        })

@app.route('/api/send-single-invitation', methods=['POST'])
@admin_required
def send_single_invitation():
    """Send invitation to a single member"""
    data = request.get_json()
    member_id = data.get('member_id')
    
    if not member_id:
        return jsonify({
            'success': False,
            'message': 'Member ID is required'
        })
    
    try:
        # Get member data from database
        conn = sqlite3.connect('aga_attendance.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM members WHERE member_id = ?', (member_id,))
        member = cursor.fetchone()
        conn.close()
        
        if not member:
            return jsonify({
                'success': False,
                'message': 'Member not found'
            })
        
        from email_service import EmailService
        email_service = EmailService()
        
        success, message = email_service.send_single_invitation(
            member[1],  # member_id
            member[2],  # full_name
            member[3],  # email
            member[5]   # qr_code
        )
        
        return jsonify({
            'success': success,
            'message': message,
            'member': member[2]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error sending invitation: {str(e)}'
        })

@app.route('/api/toggle-checkin', methods=['POST'])
@admin_required
def toggle_checkin():
    """Toggle member check-in status (admin function)"""
    data = request.get_json()
    member_id = data.get('member_id')
    check_in = data.get('check_in')
    
    if not member_id or check_in is None:
        return jsonify({
            'success': False,
            'message': 'Missing required parameters'
        })
    
    conn = sqlite3.connect('aga_attendance.db')
    cursor = conn.cursor()
    
    try:
        # Check if member exists
        cursor.execute('SELECT full_name FROM members WHERE member_id = ?', (member_id,))
        member = cursor.fetchone()
        
        if not member:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Member not found'
            })
        
        # Update check-in status
        if check_in:
            cursor.execute('''
                UPDATE members 
                SET checked_in = TRUE, check_in_time = CURRENT_TIMESTAMP 
                WHERE member_id = ?
            ''', (member_id,))
            action = 'checked in'
        else:
            cursor.execute('''
                UPDATE members 
                SET checked_in = FALSE, check_in_time = NULL 
                WHERE member_id = ?
            ''', (member_id,))
            action = 'checked out'
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Member {member[0]} has been {action} successfully'
        })
        
    except Exception as e:
        conn.close()
        return jsonify({
            'success': False,
            'message': f'Error updating member status: {str(e)}'
        })

@app.route('/api/bulk-checkout', methods=['POST'])
@admin_required
def bulk_checkout():
    """Check out all members (admin function)"""
    conn = sqlite3.connect('aga_attendance.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE members 
            SET checked_in = FALSE, check_in_time = NULL 
            WHERE checked_in = TRUE
        ''')
        
        affected_rows = cursor.rowcount
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': f'Successfully checked out {affected_rows} members'
        })
        
    except Exception as e:
        conn.close()
        return jsonify({
            'success': False,
            'message': f'Error checking out members: {str(e)}'
        })

@app.route('/api/reset-checkins', methods=['POST'])
@admin_required
def reset_checkins():
    """Reset all check-ins (admin function)"""
    conn = sqlite3.connect('aga_attendance.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            UPDATE members 
            SET checked_in = FALSE, check_in_time = NULL
        ''')
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'All check-ins have been reset successfully'
        })
        
    except Exception as e:
        conn.close()
        return jsonify({
            'success': False,
            'message': f'Error resetting check-ins: {str(e)}'
        })

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
