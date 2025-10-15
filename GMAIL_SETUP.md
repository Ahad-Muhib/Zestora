# Gmail Setup for Password Reset Emails

## Step 1: Enable 2-Factor Authentication on Gmail
1. Go to your Google Account settings
2. Navigate to "Security"
3. Enable "2-Step Verification"

## Step 2: Generate App Password
1. In Google Account Security settings
2. Find "App passwords" (may need to scroll down)
3. Select "Mail" as the app
4. Select "Other" as the device
5. Name it "Django Zestora" 
6. Google will generate a 16-character password like: `abcd efgh ijkl mnop`

## Step 3: Set Environment Variables

### On Linux/Mac (Terminal):
```bash
export EMAIL_HOST_USER="your-email@gmail.com"
export EMAIL_HOST_PASSWORD="abcd efgh ijkl mnop"
```

### On Windows (Command Prompt):
```cmd
set EMAIL_HOST_USER=your-email@gmail.com
set EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
```

### Or create a .env file:
```
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
```

## Step 4: Test the Setup
```bash
cd /home/muhib/muhib/project/Zestora
source venv/bin/activate
python manage.py shell
```

Then in the shell:
```python
from django.core.mail import send_mail
send_mail(
    'Test from Zestora',
    'This is a test email!',
    'your-email@gmail.com',
    ['recipient@example.com']
)
```

## Step 5: Restart Django Server
```bash
python manage.py runserver 8002
```

## Security Notes:
- Never commit your app password to Git
- Use environment variables or .env files
- The app password is different from your regular Gmail password
- App passwords are specific to each application

## Alternative Email Providers:
- **SendGrid**: Professional email service
- **Mailgun**: Good for developers
- **AWS SES**: If using AWS
- **Outlook/Hotmail**: Similar setup to Gmail