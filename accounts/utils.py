import os
import random
import string

import requests
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
        'login': 'Fernwood & Co. - Your login OTP',
        'reset': 'Fernwood & Co. - Password reset code',
    }
    messages = {
        'register': f"Hi {name},\n\nYour verification code is: {code}\n\nExpires in {expiry} minutes.\n\n- Fernwood & Co.",
        'login': f"Hi {name},\n\nYour login OTP is: {code}\n\nExpires in {expiry} minutes.\n\n- Fernwood & Co.",
        'reset': f"Hi {name},\n\nYour password reset code is: {code}\n\nExpires in {expiry} minutes.\n\n- Fernwood & Co.",
    }

    resp = requests.post(
        "https://api.brevo.com/v3/smtp/email",
        headers={
            "api-key": os.environ["BREVO_API_KEY"],
            "accept": "application/json",
            "content-type": "application/json",
        },
        json={
            "sender": {"name": "Fernwood & Co.", "email": os.environ["BREVO_SENDER_EMAIL"]},
            "to": [{"email": user.email}],
            "subject": subjects[purpose],
            "textContent": messages[purpose],
        },
        timeout=10,
    )
    resp.raise_for_status()
    return code