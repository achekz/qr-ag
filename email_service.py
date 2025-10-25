"""
Email service for sending QR code invitations
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from io import BytesIO
import qrcode
from config import Config

class EmailService:
    def __init__(self):
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.username = Config.SMTP_USERNAME
        self.password = Config.SMTP_PASSWORD
    
    def generate_qr_code_image(self, qr_data, member_name):
        """Generate QR code image"""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=Config.QR_CODE_SIZE,
            border=Config.QR_CODE_BORDER,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Add member name to image
        from PIL import Image, ImageDraw, ImageFont
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        text = f"Member: {member_name}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        img_width, img_height = img.size
        x = (img_width - text_width) // 2
        y = img_height - text_height - 10
        
        draw.text((x, y), text, fill="black", font=font)
        
        return img
    
    def create_email_content(self, member_name, qr_data):
        """Create HTML email content with registration information"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Registration Confirmation - {Config.EVENT_NAME}</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; margin: 0; padding: 0;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #ffffff;">
                <!-- Header -->
                <div style="text-align: center; margin-bottom: 30px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px 20px; border-radius: 10px;">
                    <h1 style="margin: 0; font-size: 28px; font-weight: bold;">{Config.EVENT_NAME}</h1>
                    <h2 style="margin: 10px 0 0 0; font-size: 18px; font-weight: normal; opacity: 0.9;">Registration Confirmation</h2>
                </div>
                
                <!-- Main Content -->
                <div style="background-color: #f8f9fa; padding: 25px; border-radius: 10px; margin-bottom: 20px; border-left: 4px solid #667eea;">
                    <h3 style="color: #2c3e50; margin-top: 0; font-size: 22px;">Dear {member_name},</h3>
                    
                    <div style="background-color: #fff3cd; padding: 15px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #ffc107;">
                        <p style="margin: 0; font-weight: bold; color: #856404;">
                            <strong>Registration Status:</strong> Registration is now closed due to very high interest. 
                            All confirmed registrants will receive a personal QR code by email and WhatsApp—please present it with a valid ID (CIN or passport) at the hotel entrance.
                        </p>
                    </div>
                    
                    <p style="font-size: 16px; margin: 20px 0;">We look forward to welcoming you to our <strong>{Config.EVENT_NAME}</strong>!</p>
                    
                    <div style="background-color: white; padding: 20px; border-radius: 8px; margin: 20px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <h4 style="margin-top: 0; color: #2c3e50; font-size: 18px;">📅 Event Details:</h4>
                        <div style="margin: 15px 0;">
                            <p style="margin: 8px 0; font-size: 16px;"><strong>📅 Date:</strong> {Config.EVENT_DATE}</p>
                            <p style="margin: 8px 0; font-size: 16px;"><strong>🕐 Time:</strong> {Config.EVENT_TIME}</p>
                            <p style="margin: 8px 0; font-size: 16px;"><strong>📍 Venue:</strong> {Config.EVENT_VENUE}</p>
                        </div>
                    </div>
                </div>
                
                <!-- QR Code Section -->
                <div style="text-align: center; margin: 30px 0; background-color: #f8f9fa; padding: 25px; border-radius: 10px;">
                    <h3 style="color: #2c3e50; margin-top: 0; font-size: 20px;">🎫 Your Personal QR Code</h3>
                    <p style="color: #6c757d; font-size: 16px; margin: 15px 0;">Please present this QR code at the entrance for verification</p>
                    <div style="border: 3px dashed #667eea; padding: 25px; margin: 20px 0; border-radius: 10px; background-color: white;">
                        <p style="margin: 0; color: #6c757d; font-size: 14px; font-style: italic;">QR Code attached as image below</p>
                    </div>
                </div>
                
                <!-- Important Instructions -->
                <div style="background-color: #e8f4fd; padding: 20px; border-radius: 10px; margin: 20px 0; border-left: 4px solid #17a2b8;">
                    <h4 style="color: #2c3e50; margin-top: 0; font-size: 18px;">⚠️ Important Instructions:</h4>
                    <ul style="margin: 15px 0; padding-left: 25px; font-size: 15px;">
                        <li style="margin: 8px 0;"><strong>Valid ID Required:</strong> Bring your CIN or passport for verification</li>
                        <li style="margin: 8px 0;"><strong>QR Code:</strong> Present your QR code at the hotel entrance</li>
                        <li style="margin: 8px 0;"><strong>Arrival Time:</strong> Please arrive on time for smooth check-in</li>
                        <li style="margin: 8px 0;"><strong>Keep This Email:</strong> Save this email and QR code for your records</li>
                        <li style="margin: 8px 0;"><strong>Contact:</strong> Reach out if you have any questions</li>
                    </ul>
                </div>
                
                <!-- Footer -->
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 2px solid #ecf0f1;">
                    <p style="color: #6c757d; font-size: 14px; margin: 10px 0;">
                        <strong>TIPCS AGA25</strong> - Annual General Assembly
                    </p>
                    <p style="color: #adb5bd; font-size: 12px; margin: 5px 0;">
                        This is an automated confirmation email. Please do not reply to this email.
                    </p>
                </div>
            </div>
        </body>
        </html>
        """
        return html_content
    
    def send_invitation(self, member_name, email, qr_data):
        """Send invitation email with QR code"""
        if not self.username or not self.password:
            return False, "Email credentials not configured"
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.username
            msg['To'] = email
            msg['Subject'] = f"Registration Confirmation - {Config.EVENT_NAME} - Your Personal QR Code"
            
            # Create HTML content
            html_content = self.create_email_content(member_name, qr_data)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Generate and attach QR code image
            qr_img = self.generate_qr_code_image(qr_data, member_name)
            img_buffer = BytesIO()
            qr_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            img_attachment = MIMEImage(img_buffer.read())
            img_attachment.add_header('Content-Disposition', 'attachment', filename=f'qr-code-{member_name.replace(" ", "-")}.png')
            msg.attach(img_attachment)
            
            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(msg)
            server.quit()
            
            return True, "Email sent successfully"
            
        except Exception as e:
            return False, f"Error sending email: {str(e)}"
    
    def send_bulk_invitations(self, members, batch_size=10, delay_seconds=1):
        """Send invitations to multiple members with rate limiting"""
        import time
        results = []
        total_members = len(members)
        
        for i, member in enumerate(members):
            if member.get('email'):
                success, message = self.send_invitation(
                    member['full_name'],
                    member['email'],
                    member['qr_code']
                )
                results.append({
                    'member': member['full_name'],
                    'email': member['email'],
                    'success': success,
                    'message': message
                })
            else:
                results.append({
                    'member': member['full_name'],
                    'email': member.get('email', 'No email'),
                    'success': False,
                    'message': 'No email address provided'
                })
            
            # Rate limiting: pause after every batch_size emails
            if (i + 1) % batch_size == 0 and i < total_members - 1:
                time.sleep(delay_seconds)
        
        return results
    
    def send_single_invitation(self, member_id, member_name, email, qr_data):
        """Send invitation to a single member"""
        if not email:
            return False, "No email address provided"
        
        return self.send_invitation(member_name, email, qr_data)
    
    def get_email_stats(self, results):
        """Get statistics from email sending results"""
        total = len(results)
        successful = len([r for r in results if r['success']])
        failed = total - successful
        
        return {
            'total': total,
            'successful': successful,
            'failed': failed,
            'success_rate': (successful / total * 100) if total > 0 else 0
        }
