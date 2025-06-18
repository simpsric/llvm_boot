import os, sys
from dotenv import load_dotenv
from google.genai import types, Client

param_count = len(sys.argv)
print(param_count)

if param_count < 2:
    print("Usage: python main.py <prompt>")
    sys.exit(1)

prompt = sys.argv[1]

if param_count >= 3 and sys.argv[2] == "--verbose":
    b_verbose_set = True
else:
    b_verbose_set = False

messages = [
    types.Content(role="user", parts=[types.Part(text=prompt)])
]

# Load environment variables from .env file
load_dotenv()
# Get the value of the environment variable
API_KEY = os.getenv('GEMINI_API_KEY')

client = Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=messages
)

print(response.text)
if b_verbose_set:
    print(f"User prompt: {prompt}")
    print("Prompt tokens:", response.usage_metadata.prompt_token_count)
    print("Response tokens:", response.usage_metadata.candidates_token_count)
    