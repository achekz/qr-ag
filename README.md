# AGA QR Code System

A comprehensive QR code generation and attendance verification system for the 2025 TIPCS Annual General Assembly.

## 🚀 Features

- **Member Management**: Import 224+ members from CSV file
- **QR Code Generation**: Unique QR codes for each member
- **Real-time Verification**: Desktop and mobile verification interfaces
- **Attendance Tracking**: Live statistics and member status
- **Email Integration**: Send digital invitations with QR codes
- **Mobile-Friendly**: Responsive design for all devices

## 📋 Requirements

- Python 3.8+
- Flask
- Pandas
- QRCode
- Pillow
- SQLite

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/achekz/qr-ag.git
   cd qr-ag
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the system:**
   - Home: http://localhost:5000
   - Admin: http://localhost:5000/admin
   - Verify: http://localhost:5000/verify
   - Mobile: http://localhost:5000/mobile

## 🌐 Deployment Options

### Option 1: Railway (Recommended)

1. **Sign up at [Railway](https://railway.app)**
2. **Connect your GitHub repository**
3. **Deploy automatically** - Railway will detect the Flask app
4. **Your app will be live** at a Railway URL

### Option 2: Heroku

1. **Install Heroku CLI**
2. **Login to Heroku:**
   ```bash
   heroku login
   ```
3. **Create Heroku app:**
   ```bash
   heroku create your-app-name
   ```
4. **Deploy:**
   ```bash
   git push heroku main
   ```

### Option 3: Render

1. **Sign up at [Render](https://render.com)**
2. **Connect GitHub repository**
3. **Select "Web Service"**
4. **Configure:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
5. **Deploy**

### Option 4: PythonAnywhere

1. **Sign up at [PythonAnywhere](https://pythonanywhere.com)**
2. **Upload your files**
3. **Configure web app**
4. **Set up virtual environment**
5. **Install requirements and run**

## 📁 Project Structure

```
qr-ag/
├── app.py                          # Main Flask application
├── config.py                       # Configuration settings
├── email_service.py                # Email service for invitations
├── requirements.txt                # Python dependencies
├── Procfile                        # Deployment configuration
├── runtime.txt                     # Python version
├── templates/                      # HTML templates
│   ├── base.html                   # Base template
│   ├── index.html                  # Home page
│   ├── admin.html                  # Admin panel
│   ├── verify.html                 # Desktop verification
│   └── mobile.html                 # Mobile verification
├── 2025_TIPCS_Annual_General_Assembly_(AGA25).csv  # Member data
└── README.md                       # This file
```

## 🔧 Configuration

### Email Settings (Optional)
To enable email invitations, set these environment variables:
- `SMTP_SERVER`: Your SMTP server
- `SMTP_PORT`: SMTP port (usually 587)
- `SMTP_USERNAME`: Your email username
- `SMTP_PASSWORD`: Your email password

### Event Details
Update `config.py` with your event information:
- Event name
- Date and time
- Venue location

## 📱 Usage

### Admin Panel
1. **Load Members**: Click "Load Members from CSV" to import all members
2. **Generate QR Codes**: QR codes are automatically generated
3. **Send Invitations**: Use the email service to send invitations
4. **Monitor Attendance**: View real-time statistics

### Verification
1. **Desktop**: Use `/verify` for staff verification
2. **Mobile**: Use `/mobile` for mobile devices
3. **Scan QR Codes**: Enter QR code data manually or scan
4. **Real-time Updates**: See attendance statistics instantly

## 🎯 Key Features

- **224 Members**: Pre-loaded from CSV file
- **Unique QR Codes**: Each member gets a unique identifier
- **Real-time Tracking**: Live attendance monitoring
- **Mobile Support**: Works on all devices
- **Email Integration**: Send digital invitations
- **Duplicate Prevention**: Prevents multiple check-ins
- **Statistics Dashboard**: Real-time attendance data

## 🔒 Security

- Unique QR codes with hash verification
- Database-backed attendance tracking
- Duplicate prevention system
- Secure member verification

## 📞 Support

For issues or questions:
- Check the GitHub repository
- Review the deployment logs
- Ensure all dependencies are installed
- Verify CSV file format

## 🚀 Quick Start

1. **Clone and install:**
   ```bash
   git clone https://github.com/achekz/qr-ag.git
   cd qr-ag
   pip install -r requirements.txt
   ```

2. **Run locally:**
   ```bash
   python app.py
   ```

3. **Deploy to cloud:**
   - Railway: Connect GitHub repo
   - Heroku: `git push heroku main`
   - Render: Connect GitHub repo

Your AGA QR Code System is ready for the 2025 TIPCS Annual General Assembly! 🎉