#!/bin/bash

# Quick Gmail Setup Script for Zestora Password Reset

echo "🔧 Gmail Setup for Zestora Password Reset"
echo "========================================"

echo ""
echo "📧 Please provide your Gmail credentials:"
read -p "Enter your Gmail address: " gmail_address
read -s -p "Enter your Gmail App Password (16 chars): " app_password
echo ""

echo ""
echo "Setting environment variables..."
export EMAIL_HOST_USER="$gmail_address"
export EMAIL_HOST_PASSWORD="$app_password"

echo "✅ Environment variables set!"
echo ""

echo "🧪 Testing email configuration..."
cd /home/muhib/muhib/project/Zestora
source venv/bin/activate

python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zestora.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

print(f'📤 Sending test email from: {settings.EMAIL_HOST_USER}')
print(f'📧 To: $gmail_address')

try:
    send_mail(
        'Zestora Test Email',
        'Congratulations! Your Gmail integration is working correctly. You can now receive password reset emails.',
        settings.DEFAULT_FROM_EMAIL,
        ['$gmail_address'],
        fail_silently=False,
    )
    print('✅ Test email sent successfully!')
    print('📬 Check your Gmail inbox (and spam folder)')
except Exception as e:
    print(f'❌ Error sending email: {e}')
    print('💡 Make sure you:')
    print('   1. Enabled 2FA on Gmail')
    print('   2. Generated an App Password (not your regular password)')
    print('   3. Used the correct 16-character app password')
"

echo ""
echo "🚀 Starting Django server..."
python manage.py runserver 8002