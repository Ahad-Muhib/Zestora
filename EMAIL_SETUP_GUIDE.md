# Email Configuration Options for Zestora

## Option 1: Gmail SMTP (Recommended for development)
# 1. Enable 2-factor authentication on your Gmail account
# 2. Generate an "App Password" for Django
# 3. Add to your environment variables:
#    EMAIL_HOST_USER=your-email@gmail.com
#    EMAIL_HOST_PASSWORD=your-app-password

## Option 2: SendGrid (Recommended for production)
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.sendgrid.net'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = 'apikey'
# EMAIL_HOST_PASSWORD = os.getenv('SENDGRID_API_KEY')

## Option 3: AWS SES (For AWS deployments)
# EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
# AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
# AWS_SES_REGION_NAME = 'us-east-1'

## Option 4: Development Console Backend (For testing)
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# This will print emails to the console instead of sending them

## To test email functionality:
# python manage.py shell
# from django.core.mail import send_mail
# send_mail('Test', 'This is a test email', 'from@example.com', ['to@example.com'])