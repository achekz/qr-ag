@echo off
echo Setting up email environment variables...

set SMTP_USERNAME=tipcs.devices@gmail.com
set SMTP_PASSWORD=dptd jwnt vfsh eeci
set SMTP_SERVER=smtp.gmail.com
set SMTP_PORT=587

echo Environment variables set:
echo SMTP_USERNAME=%SMTP_USERNAME%
echo SMTP_SERVER=%SMTP_SERVER%
echo SMTP_PORT=%SMTP_PORT%
echo SMTP_PASSWORD=***hidden***

echo.
echo Testing email configuration...
python test_email.py

pause
