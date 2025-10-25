# Email Configuration Guide

## Quick Setup for Gmail

### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Settings](https://myaccount.google.com/)
2. Click on "Security" in the left sidebar
3. Under "Signing in to Google", click "2-Step Verification"
4. Follow the setup process

### Step 2: Generate App Password
1. In Google Account Settings, go to "Security"
2. Under "Signing in to Google", click "App passwords"
3. Select "Mail" as the app
4. Copy the 16-character password that appears

### Step 3: Set Environment Variables
```bash
# Windows (Command Prompt)
set SMTP_USERNAME=your-email@gmail.com
set SMTP_PASSWORD=your-16-character-app-password

# Windows (PowerShell)
$env:SMTP_USERNAME="your-email@gmail.com"
$env:SMTP_PASSWORD="your-16-character-app-password"

# Linux/Mac
export SMTP_USERNAME="your-email@gmail.com"
export SMTP_PASSWORD="your-16-character-app-password"
```

### Step 4: Test Configuration
```bash
python test_email.py
```

## Alternative Email Providers

### Outlook/Hotmail
```bash
export SMTP_SERVER="smtp-mail.outlook.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@outlook.com"
export SMTP_PASSWORD="your-password"
```

### Yahoo Mail
```bash
export SMTP_SERVER="smtp.mail.yahoo.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@yahoo.com"
export SMTP_PASSWORD="your-app-password"
```

### Custom SMTP Server
```bash
export SMTP_SERVER="smtp.your-domain.com"
export SMTP_PORT="587"
export SMTP_USERNAME="your-email@your-domain.com"
export SMTP_PASSWORD="your-password"
```

## Troubleshooting

### Common Error Messages

**"Authentication failed"**
- Check username and password
- For Gmail, ensure you're using App Password, not regular password
- Verify 2FA is enabled

**"Connection refused"**
- Check SMTP server and port settings
- Ensure firewall allows SMTP connections
- Try different ports (465 for SSL, 587 for TLS)

**"Rate limit exceeded"**
- Reduce batch size in email settings
- Increase delay between batches
- Check your email provider's sending limits

### Testing Email Configuration

Run the test script to verify everything works:

```bash
python test_email.py
```

If prompted, enter a test email address to receive a sample email.

## Security Notes

- Never commit email credentials to version control
- Use environment variables for sensitive data
- Consider using a dedicated email account for sending
- Monitor sending limits to avoid account suspension
