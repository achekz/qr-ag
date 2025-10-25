# TIPCS AGA25 Email System

This document explains how to use the enhanced email system for sending registration confirmations with QR codes to TIPCS AGA25 participants.

## 📧 Email System Features

- **Professional Email Templates**: Beautiful HTML emails with registration information
- **QR Code Attachments**: Personal QR codes attached to each email
- **Bulk Email Sending**: Send to all members or selected groups
- **Individual Email Sending**: Send emails to specific members
- **Rate Limiting**: Configurable batch sizes and delays to prevent spam
- **Progress Tracking**: Real-time progress updates during bulk sending
- **Error Handling**: Comprehensive error reporting and retry mechanisms

## 🚀 Quick Start

### 1. Configure Email Settings

Set up your SMTP credentials as environment variables:

```bash
# For Gmail (recommended)
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"

# For other providers
export SMTP_USERNAME="your-email@domain.com"
export SMTP_PASSWORD="your-password"
export SMTP_SERVER="smtp.your-provider.com"
export SMTP_PORT="587"
```

### 2. Test Email Configuration

Run the test script to verify your email setup:

```bash
python test_email.py
```

### 3. Start the Application

```bash
python app.py
```

### 4. Access Admin Panel

Navigate to `http://localhost:5000/admin` and login with:
- Username: `admin`
- Password: `admintipcs`

## 📱 Using the Email System

### Admin Panel Features

1. **Load Members**: Click "Load Members from CSV" to import all participants
2. **Send Registration Emails**: Click "Send Registration Emails" to open the email modal
3. **Individual Emails**: Click the email icon next to any member's name

### Email Sending Options

#### Option 1: Send to All Members
- Select "Send to All Members"
- Choose batch size (5, 10, 20, or 50 emails per batch)
- Set delay between batches (1, 2, or 5 seconds)
- Click "Send Emails"

#### Option 2: Send to Individual Member
- Select "Send to Individual Member"
- Choose a member from the dropdown
- Click "Send Emails"

#### Option 3: Send to Selected Members
- Select "Send to Selected Members"
- Configure batch settings
- Click "Send Emails"

### Email Content

Each email includes:

- **Subject**: "Registration Confirmation - TIPCS AGA25 - Your Personal QR Code"
- **Professional HTML Design**: Modern, responsive email template
- **Registration Status**: Information about closed registration
- **Event Details**: Date, time, and venue information
- **QR Code Attachment**: Personal QR code as PNG image
- **Important Instructions**: ID requirements and check-in procedures

## 🔧 Configuration

### Event Details

Update `config.py` with your event information:

```python
EVENT_NAME = "TIPCS AGA25"
EVENT_DATE = "Sunday, 26 October 2025"
EVENT_TIME = "08:00"
EVENT_VENUE = "Hotel Delphin El Habib, Monastir"
```

### Email Settings

Configure SMTP settings in `config.py` or via environment variables:

```python
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
```

## 📊 Email Statistics

The system provides detailed statistics after bulk email sending:

- **Total Emails**: Number of emails attempted
- **Successful**: Number of emails sent successfully
- **Failed**: Number of emails that failed
- **Success Rate**: Percentage of successful sends

## 🛠️ Troubleshooting

### Common Issues

1. **"Email credentials not configured"**
   - Set SMTP_USERNAME and SMTP_PASSWORD environment variables
   - For Gmail, use App Password instead of regular password

2. **"Authentication failed"**
   - Check username and password
   - For Gmail, ensure 2FA is enabled and App Password is used

3. **"Connection refused"**
   - Check SMTP_SERVER and SMTP_PORT settings
   - Ensure firewall allows SMTP connections

4. **"Rate limit exceeded"**
   - Reduce batch size
   - Increase delay between batches
   - Check your email provider's sending limits

### Gmail Setup

1. **Enable 2-Factor Authentication**
   - Go to Google Account settings
   - Security > 2-Step Verification
   - Follow the setup process

2. **Generate App Password**
   - Go to Google Account settings
   - Security > 2-Step Verification > App passwords
   - Select "Mail" and generate password
   - Use this password as SMTP_PASSWORD

3. **Configure Environment Variables**
   ```bash
   export SMTP_USERNAME="your-email@gmail.com"
   export SMTP_PASSWORD="your-16-character-app-password"
   ```

## 📈 Best Practices

### Email Sending

1. **Start Small**: Test with individual emails before bulk sending
2. **Use Rate Limiting**: Configure appropriate batch sizes and delays
3. **Monitor Results**: Check success rates and handle failures
4. **Backup Plan**: Keep a list of failed sends for manual retry

### Content Management

1. **Preview Emails**: Review email content before sending
2. **Test QR Codes**: Verify QR codes work with verification system
3. **Update Information**: Keep event details current
4. **Professional Tone**: Maintain professional communication

## 🔒 Security Considerations

1. **Credentials**: Never commit SMTP credentials to version control
2. **Environment Variables**: Use environment variables for sensitive data
3. **Rate Limiting**: Respect email provider limits
4. **Data Privacy**: Ensure compliance with data protection regulations

## 📞 Support

For issues or questions:

1. **Check Configuration**: Verify SMTP settings and credentials
2. **Run Tests**: Use `test_email.py` to diagnose issues
3. **Review Logs**: Check application logs for error details
4. **Email Provider**: Contact your email provider for SMTP issues

## 🎯 Success Metrics

- **Delivery Rate**: Aim for >95% successful delivery
- **Open Rate**: Monitor email open rates (if tracking enabled)
- **Response Time**: Track time from sending to delivery
- **Error Rate**: Monitor and minimize failed sends

---

**Ready to send registration emails for TIPCS AGA25!** 🎉

For technical support or questions, refer to the main project documentation or contact the development team.
