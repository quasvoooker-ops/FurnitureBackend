import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP


def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def send_otp_email(user, purpose):
    OTP.objects.filter(user=user, purpose=purpose, is_used=False).update(is_used=True)
    code = generate_otp()
    OTP.objects.create(user=user, code=code, purpose=purpose)

    expiry = getattr(settings, 'OTP_EXPIRY_MINUTES', 10)
    name = user.first_name or user.username

    subjects = {
        'register': 'Fernwood & Co. - Verify your email',
        'login':    'Fernwood & Co. - Your login OTP',
        'reset':    'Fernwood & Co. - Password reset code',
    }
    messages = {
        'register': f"Hi {name},\n\nYour verification code is: {code}\n\nExpires in {expiry} minutes.\n\n- Fernwood & Co.",
        'login':    f"Hi {name},\n\nYour login OTP is: {code}\n\nExpires in {expiry} minutes.\n\n- Fernwood & Co.",
        'reset':    f"Hi {name},\n\nYour password reset code is: {code}\n\nExpires in {expiry} minutes.\n\n- Fernwood & Co.",
    }

    send_mail(
        subjects[purpose],
        messages[purpose],
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
    return code
