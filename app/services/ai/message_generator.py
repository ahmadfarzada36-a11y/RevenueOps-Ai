from openai import AsyncOpenAI
from app.core.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

async def generate_followup_message(company, contact, deal_value):

    prompt = f"""
    Write a professional B2B follow-up email.

    Company: {company}
    Contact: {contact}
    Deal value: {deal_value}

    Make it persuasive but short.
    """

    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content