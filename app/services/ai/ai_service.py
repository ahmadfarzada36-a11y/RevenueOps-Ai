import os
import openai
import asyncio
from typing import Optional

# API Key امن از environment
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY environment variable is missing")

openai.api_key = OPENAI_API_KEY

async def generate_followup_message(client_name: str, deal_status: str, days_since_quote: int) -> str:
    """
    Async wrapper حرفه‌ای برای OpenAI
    """
    prompt = f"""
Generate a concise, polite, and persuasive follow-up message for a B2B client.
Client: {client_name}
Deal Status: {deal_status}
Days since quotation: {days_since_quote}
"""
    # اجرای synchronous OpenAI call در executor تا event loop بلوکه نشود
    loop = asyncio.get_running_loop()
    try:
        response = await loop.run_in_executor(
            None,
            lambda: openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=150
            )
        )
        return response.choices[0].message.content.strip()
    except openai.error.OpenAIError as e:
        print(f"❌ OpenAI API error: {e}")
        return "Follow-up message could not be generated at this time."
    except Exception as e:
        print(f"❌ Unexpected error in AI service: {e}")
        return "Follow-up message could not be generated at this time."