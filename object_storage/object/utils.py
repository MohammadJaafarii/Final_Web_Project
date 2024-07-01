# utils.py

import hashlib
import time
from .models import TempUser
from django.conf import settings

def generate_email_verification_token(email):
    token = hashlib.sha256(f'{email}{time.time()}'.encode()).hexdigest()
    return token

def verify_email_verification_token(token):
    try:
        temp_user = TempUser.objects.get(token=token)
        return temp_user.email
    except TempUser.DoesNotExist:
        return None
