# test_gemini_key.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from google import genai

api_key = getattr(settings, 'GEMINI_API_KEY', None)
print(f"API Key: {api_key[:20] if api_key else 'None'}...")

if not api_key:
    print("❌ No API key found!")
    exit()

try:
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp",
        contents="Return ONLY JSON: {'language': 'Python'}"
    )
    print("✅ API Key is VALID!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ API Key is INVALID: {e}")