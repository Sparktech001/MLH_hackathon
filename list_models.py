import os
import requests
from dotenv import load_dotenv
load_dotenv('.env')

api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    print('No API key found in .env')
    exit(1)

url = f'https://generativelanguage.googleapis.com/v1beta/models?key={api_key}'
response = requests.get(url)

if response.status_code == 200:
    models = response.json().get('models', [])
    for m in models:
        print(f"{m['name']} - Supported methods: {m.get('supportedGenerationMethods', [])}")
else:
    print('Failed to list models:', response.text)
