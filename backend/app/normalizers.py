import re
import hmac
import hashlib
from app.config import settings

def normalize_email(email: str) -> str:
    if not email:
        return ""
    return email.strip().lower()

def normalize_phone(phone: str) -> str:
    if not phone:
        return ""
    # Remove whitespace, hyphens, brackets
    cleaned = re.sub(r'[\s\-()]+', '', phone)
    has_plus = cleaned.startswith('+')
    digits = re.sub(r'\D', '', cleaned)
    return f"+{digits}" if has_plus else digits

def normalize_upi(upi: str) -> str:
    if not upi:
        return ""
    return upi.strip().lower()

def hash_contact(value: str) -> str:
    if not value:
        return ""
    # HMAC-SHA256 using HASH_PEPPER
    key = settings.HASH_PEPPER.encode('utf-8')
    msg = value.encode('utf-8')
    return hmac.new(key, msg, hashlib.sha256).hexdigest()
