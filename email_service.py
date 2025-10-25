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
        """Create HTML email content"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Invitation to {Config.EVENT_NAME}</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #2c3e50;">{Config.EVENT_NAME}</h1>
                    <h2 style="color: #34495e;">Digital Invitation</h2>
                </div>
                
                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h3 style="color: #2c3e50; margin-top: 0;">Dear {member_name},</h3>
                    <p>You are cordially invited to attend our <strong>{Config.EVENT_NAME}</strong>.</p>
                    
                    <div style="background-color: white; padding: 15px; border-radius: 5px; margin: 15px 0;">
                        <h4 style="margin-top: 0; color: #2c3e50;">Event Details:</h4>
                        <p><strong>Date:</strong> {Config.EVENT_DATE}</p>
                        <p><strong>Time:</strong> {Config.EVENT_TIME}</p>
                        <p><strong>Venue:</strong> {Config.EVENT_VENUE}</p>
                    </div>
                </div>
                
                <div style="text-align: center; margin: 30px 0;">
                    <h3 style="color: #2c3e50;">Your Digital Invitation QR Code</h3>
                    <p style="color: #7f8c8d;">Please present this QR code at the entrance for verification</p>
                    <div style="border: 2px dashed #bdc3c7; padding: 20px; margin: 20px 0; border-radius: 8px;">
                        <p style="margin: 0; color: #7f8c8d;">QR Code will be attached as image</p>
                    </div>
                </div>
                
                <div style="background-color: #e8f4fd; padding: 15px; border-radius: 5px; margin: 20px 0;">
                    <h4 style="color: #2c3e50; margin-top: 0;">Important Instructions:</h4>
                    <ul style="margin: 10px 0; padding-left: 20px;">
                        <li>Please arrive 15 minutes before the event starts</li>
                        <li>Present your QR code at the entrance for verification</li>
                        <li>Keep this email and QR code for your records</li>
                        <li>Contact us if you have any questions</li>
                    </ul>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ecf0f1;">
                    <p style="color: #7f8c8d; font-size: 14px;">
                        This is an automated invitation. Please do not reply to this email.
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
            msg['Subject'] = f"Invitation to {Config.EVENT_NAME} - Digital QR Code"
            
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
    
    def send_bulk_invitations(self, members):
        """Send invitations to multiple members"""
        results = []
        
        for member in members:
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
                    'email': member['email'],
                    'success': False,
                    'message': 'No email address provided'
                })
        
        return results
