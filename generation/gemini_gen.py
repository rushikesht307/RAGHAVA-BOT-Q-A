from dotenv import load_dotenv
from google import genai
import os

model = "gemini-3.1-flash-lite"


def main(sys_prompt):
    load_dotenv()

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    if not GEMINI_API_KEY:
        return "GEMINI_API_KEY is not configured."

    client = genai.Client(api_key=GEMINI_API_KEY)

    response = client.models.generate_content(
        model=model,
        contents=sys_prompt
    )

    return response.text