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
        """Create modern HTML invitation email content"""
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>{Config.EVENT_NAME} - Your Access Pass</title>
        </head>
        <body style="font-family: Arial, sans-serif; background-color: #f4f6f8; margin: 0; padding: 0;">
          <div style="max-width: 650px; margin: 30px auto; background-color: #ffffff; border-radius: 12px; overflow: hidden; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
            
            <!-- Header -->
            <div style="background: linear-gradient(135deg, #007bff 0%, #6610f2 100%); color: #ffffff; text-align: center; padding: 40px 20px;">
              <h1 style="margin: 0; font-size: 26px; font-weight: bold;">{Config.EVENT_NAME}</h1>
              <p style="margin: 10px 0 0 0; font-size: 16px;">Your Personal Invitation & QR Access Pass</p>
            </div>

            <!-- Body -->
            <div style="padding: 30px;">
              <h2 style="font-size: 20px; color: #333;">Dear {member_name},</h2>
              <p style="font-size: 16px; color: #555; line-height: 1.6;">
                We are delighted to confirm your successful registration for <strong>{Config.EVENT_NAME}</strong>.<br>
                Please find your personal QR access code attached below. You’ll need to present it upon arrival for entry verification.
              </p>

              <div style="margin: 25px 0; background-color: #f8f9fa; border-left: 4px solid #007bff; padding: 15px 20px; border-radius: 8px;">
                <p style="margin: 0; font-size: 15px;">
                  <strong>Event Details:</strong><br>
                  📅 <strong>Date:</strong> {Config.EVENT_DATE}<br>
                  🕓 <strong>Time:</strong> {Config.EVENT_TIME}<br>
                  📍 <strong>Venue:</strong> {Config.EVENT_VENUE}
                </p>
              </div>

              <div style="text-align: center; margin: 30px 0;">
                <h3 style="font-size: 18px; color: #333;">🎫 Your QR Access Code</h3>
                <p style="color: #777; font-size: 14px;">Please present this code at the entrance for identification.</p>
                <div style="margin: 20px auto; border: 2px dashed #007bff; padding: 25px; border-radius: 10px; width: fit-content; background: #ffffff;">
                  <p style="margin: 0; color: #999; font-style: italic; font-size: 13px;">(QR code attached as image)</p>
                </div>
              </div>

              <div style="background-color: #e8f4fd; border-left: 4px solid #17a2b8; padding: 20px; border-radius: 10px;">
                <h4 style="margin-top: 0; color: #2c3e50; font-size: 17px;">Before You Arrive:</h4>
                <ul style="font-size: 15px; color: #555; padding-left: 20px;">
                  <li>Bring a valid ID (CIN or passport).</li>
                  <li>Have your QR code ready on your phone or printed copy.</li>
                  <li>Arrive at least 15 minutes early to complete check-in.</li>
                  <li>Keep this email for your records.</li>
                </ul>
              </div>

              <p style="font-size: 14px; color: #777; margin-top: 30px;">
                For any questions, please contact our coordination team at 
                <a href="mailto:{getattr(Config, 'SUPPORT_EMAIL', 'contact@tipcs.org')}" style="color: #007bff; text-decoration: none;">
                  {getattr(Config, 'SUPPORT_EMAIL', 'contact@tipcs.org')}
                </a>.
              </p>

              <p style="font-size: 13px; color: #aaa; text-align: center; margin-top: 30px;">
                — The {Config.EVENT_NAME} Organizing Committee —
              </p>
            </div>

            <!-- Footer -->
            <div style="background-color: #f1f3f5; padding: 15px; text-align: center; font-size: 12px; color: #999;">
              <p style="margin: 0;">This is an automated message. Please do not reply.</p>
              <p style="margin: 5px 0 0 0;">© {getattr(Config, 'EVENT_YEAR', '2025')} Tunisian Institute for Peace and Conflict Studies (TIPCS)</p>
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
            msg = MIMEMultipart('alternative')
            msg['From'] = self.username
            msg['To'] = email
            msg['Subject'] = f"🎟️ Your Access Pass – {Config.EVENT_NAME}"
            
            html_content = self.create_email_content(member_name, qr_data)
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Generate and attach QR code
            qr_img = self.generate_qr_code_image(qr_data, member_name)
            img_buffer = BytesIO()
            qr_img.save(img_buffer, format='PNG')
            img_buffer.seek(0)
            
            img_attachment = MIMEImage(img_buffer.read())
            img_attachment.add_header('Content-Disposition', 'attachment', filename=f'qr-code-{member_name.replace(" ", "-")}.png')
            msg.attach(img_attachment)
            
            # Send via SMTP
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
        
        print(f"Starting bulk email sending for {total_members} members")
        
        for i, member in enumerate(members):
            print(f"Processing member {i+1}/{total_members}: {member.get('full_name', 'Unknown')}")
            
            # Check if member has required fields
            if not member.get('email'):
                print(f"No email for {member.get('full_name', 'Unknown')}")
                results.append({
                    'member': member.get('full_name', 'Unknown'),
                    'email': member.get('email', 'No email'),
                    'success': False,
                    'message': 'No email address provided'
                })
                continue
                
            if not member.get('qr_code'):
                print(f"No QR code for {member.get('full_name', 'Unknown')}")
                results.append({
                    'member': member.get('full_name', 'Unknown'),
                    'email': member.get('email', 'No email'),
                    'success': False,
                    'message': 'No QR code provided'
                })
                continue
            
            try:
                success, message = self.send_invitation(
                    member['full_name'],
                    member['email'],
                    member['qr_code']
                )
                print(f"Email result for {member['full_name']}: {success} - {message}")
                results.append({
                    'member': member['full_name'],
                    'email': member['email'],
                    'success': success,
                    'message': message
                })
            except Exception as e:
                print(f"Error sending email to {member['full_name']}: {str(e)}")
                results.append({
                    'member': member['full_name'],
                    'email': member['email'],
                    'success': False,
                    'message': f'Error: {str(e)}'
                })
            
            # Rate limiting: pause after every batch_size emails
            if (i + 1) % batch_size == 0 and i < total_members - 1:
                print(f"Batch {i+1} completed, pausing for {delay_seconds} seconds...")
                time.sleep(delay_seconds)
        
        print(f"Bulk email sending completed. Results: {len(results)}")
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
