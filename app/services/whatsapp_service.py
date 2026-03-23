import requests
from app.core.config import settings


def send_whatsapp_message(phone, message):

    payload = {
        "phone": phone,
        "message": message
    }

    headers = {
        "Authorization": f"Bearer {settings.WHATSAPP_TOKEN}"
    }

    requests.post(
        settings.WHATSAPP_API_URL,
        json=payload,
        headers=headers
    )