# test_openai.py
import openai
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings

print("=" * 50)
print("🔍 TESTING OPENAI API")
print("=" * 50)

# Check API key
api_key = getattr(settings, 'OPENAI_API_KEY', None)
print(f"API Key exists: {bool(api_key)}")
print(f"API Key: {api_key[:30]}..." if api_key else "None")

if not api_key:
    print("❌ No API key found in settings!")
    exit()

# Set API key
openai.api_key = api_key

try:
    print("\n📤 Sending test request to OpenAI...")
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a language detection expert. Return only valid JSON."},
            {"role": "user", "content": 'Return ONLY JSON: {"language": "Python", "confidence": 95}'}
        ],
        temperature=0.1,
        max_tokens=50
    )
    
    print("✅ OpenAI API is WORKING!")
    print(f"Response: {response.choices[0].message.content}")
    
except Exception as e:
    print(f"❌ OpenAI API FAILED: {e}")