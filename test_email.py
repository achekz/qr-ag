#!/usr/bin/env python3
"""
Test script for the email system
"""

import os
import sys
from email_service import EmailService

def test_email_service():
    """Test the email service functionality"""
    print("Testing Email Service...")
    
    # Check if email credentials are configured
    smtp_username = os.getenv('SMTP_USERNAME', '')
    smtp_password = os.getenv('SMTP_PASSWORD', '')
    
    if not smtp_username or not smtp_password:
        print("X Email credentials not configured!")
        print("Please set the following environment variables:")
        print("  SMTP_USERNAME=your-email@gmail.com")
        print("  SMTP_PASSWORD=your-app-password")
        print("  SMTP_SERVER=smtp.gmail.com (optional)")
        print("  SMTP_PORT=587 (optional)")
        return False
    
    print(f"[OK] Email credentials found: {smtp_username}")
    
    # Test email service initialization
    try:
        email_service = EmailService()
        print("[OK] Email service initialized successfully")
    except Exception as e:
        print(f"[ERROR] Error initializing email service: {e}")
        return False
    
    # Test QR code generation
    try:
        test_qr_data = "AGA-TEST-12345"
        test_member_name = "Test Member"
        qr_img = email_service.generate_qr_code_image(test_qr_data, test_member_name)
        print("[OK] QR code generation successful")
    except Exception as e:
        print(f"[ERROR] Error generating QR code: {e}")
        return False
    
    # Test email content creation
    try:
        html_content = email_service.create_email_content(test_member_name, test_qr_data)
        if "Registration Confirmation" in html_content and "TIPCS AGA25" in html_content:
            print("[OK] Email content generation successful")
        else:
            print("[ERROR] Email content missing expected elements")
            return False
    except Exception as e:
        print(f"[ERROR] Error creating email content: {e}")
        return False
    
    # Test email sending (only if credentials are provided)
    test_email = input("\nEnter a test email address to send a test email (or press Enter to skip): ").strip()
    
    if test_email:
        try:
            print(f"Sending test email to {test_email}...")
            success, message = email_service.send_invitation(test_member_name, test_email, test_qr_data)
            
            if success:
                print(f"[OK] Test email sent successfully: {message}")
            else:
                print(f"[ERROR] Failed to send test email: {message}")
                return False
        except Exception as e:
            print(f"[ERROR] Error sending test email: {e}")
            return False
    else:
        print("[SKIP] Skipping email sending test")
    
    print("\n[SUCCESS] All tests passed! Email system is ready to use.")
    return True

def show_configuration_help():
    """Show configuration help"""
    print("\n" + "="*60)
    print("EMAIL CONFIGURATION HELP")
    print("="*60)
    print("\nTo configure email sending, you need to set up SMTP credentials.")
    print("\nFor Gmail:")
    print("1. Enable 2-factor authentication on your Google account")
    print("2. Generate an App Password:")
    print("   - Go to Google Account settings")
    print("   - Security > 2-Step Verification > App passwords")
    print("   - Generate a password for 'Mail'")
    print("3. Set environment variables:")
    print("   export SMTP_USERNAME='your-email@gmail.com'")
    print("   export SMTP_PASSWORD='your-app-password'")
    print("\nFor other email providers:")
    print("- SMTP_SERVER: Your SMTP server (e.g., smtp.gmail.com)")
    print("- SMTP_PORT: SMTP port (usually 587)")
    print("- SMTP_USERNAME: Your email username")
    print("- SMTP_PASSWORD: Your email password")
    print("\n" + "="*60)

if __name__ == "__main__":
    print("TIPCS AGA25 Email System Test")
    print("="*40)
    
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        show_configuration_help()
    else:
        success = test_email_service()
        
        if not success:
            print("\nX Some tests failed. Run with --help for configuration assistance.")
            sys.exit(1)
        else:
            print("\n[OK] Email system is ready!")
            sys.exit(0)
