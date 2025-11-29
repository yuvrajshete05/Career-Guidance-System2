# app1/utils.py

import requests
from django.conf import settings

def get_gemini_key():
    return settings.GEMINI_API_KEY

def ask_gemini(prompt):
    if not prompt:
        return "Prompt is empty."

    API_KEY = get_gemini_key()
    URL = f"https://generativelanguage.googleapis.com/v1/models/gemini-2.5-flash:generateContent?key={API_KEY}"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    try:
        response = requests.post(URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error: {e}"
