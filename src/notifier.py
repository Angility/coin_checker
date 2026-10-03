import requests
from cryptography.fernet import Fernet

def  encrypt_message(message: str, key: str) -> bytes: 
    return Fernet(key).encrypt(message.encode('utf-8'))

def send_ntfy_notification_ecnrypted(server_url: str, topic: str, encrypted_message: bytes) -> bool:
    response = requests.post(f"{server_url}/{topic}",encrypted_message)
    return True if response.status_code == 200 else False

def send_ntfy_notification(server_url: str, topic: str, token: str, message: str) -> bool:
    
    headers = {
    "Authorization": f"Bearer {token}",
    "X-Priority": "4" # Высокий приоритет
}

    response = requests.post(f"{server_url}/{topic}",message.encode('utf-8'),headers)
    return True if response.status_code == 200 else False
