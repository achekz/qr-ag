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
    EVENT_NAME = "TIPCS AGA25"
    EVENT_DATE = "Sunday, 26 October 2025"
    EVENT_TIME = "08:00"
    EVENT_VENUE = "Hotel Delphin El Habib, Monastir"
    
    # QR Code settings
    QR_CODE_SIZE = 10
    QR_CODE_BORDER = 4
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-this')
    
    # WhatsApp settings (for future WhatsApp integration)
    WHATSAPP_API_URL = os.getenv('WHATSAPP_API_URL', '')
    WHATSAPP_ACCESS_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN', '')
