from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.FERNET_KEY)

def encrypt_password(plain_text_password):
    return fernet.encrypt(plain_text_password.encode())

def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password).decode()
