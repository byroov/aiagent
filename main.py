import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types



model = "gemini-2.0-flash-001"

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
user_prompt = sys.argv[1]

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),

]






if len(user_prompt) < 1:
    raise Exception("No prompt detected: Exit code 1")
response = client.models.generate_content(
    model="gemini-2.0-flash-001", contents=messages
)

tokens = response.usage_metadata
x = tokens.prompt_token_count
y = tokens.candidates_token_count

if "--verbose" in sys.argv:
    print(f"""
        User prompt: {user_prompt}
        Prompt tokens: {x}
        Response tokens: {y}
        """)
    



