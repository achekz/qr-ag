"""
Configuration settings for AGA QR Code System
"""

import os

class Config:
    # Database
    DATABASE_URL = 'aga_attendance.db'
    
    # Email settings (configure these for email sending)
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
    SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
    
    # Event details
    EVENT_NAME = "Annual General Assembly"
    EVENT_DATE = "2024-01-15"  # Update this with your event date
    EVENT_TIME = "10:00 AM"
    EVENT_VENUE = "Conference Hall, Main Building"
    
    # QR Code settings
    QR_CODE_SIZE = 10
    QR_CODE_BORDER = 4
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    
    # WhatsApp settings (for future WhatsApp integration)
    WHATSAPP_API_URL = os.getenv('WHATSAPP_API_URL', '')
    WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN', '')
