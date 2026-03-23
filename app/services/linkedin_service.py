import httpx
from app.core.config import settings

class LinkedInService:

    async def send_message(self, profile_id: str, message: str):

        url = "https://api.linkedin.com/v2/messages"

        headers = {
            "Authorization": f"Bearer {settings.LINKEDIN_TOKEN}"
        }

        payload = {
            "recipient": profile_id,
            "message": message
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)

        return response.json()