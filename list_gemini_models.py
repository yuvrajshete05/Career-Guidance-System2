import google.generativeai as genai
from django.conf import settings
import os

# Option 1: Try to load API key from Django settings (recommended for project context)
try:
    # This setup is needed if running as a standalone script outside a Django runserver context
    # but you still want to load settings.
    # It assumes your Django project's settings.py is accessible.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginform.settings')
    import django
    django.setup()
    API_KEY = settings.GEMINI_API_KEY
    print("API key loaded from Django settings.")
except Exception as e:
    print(f"Could not load API key from Django settings: {e}")
    # Fallback to direct key if settings loading fails
    API_KEY = None


# Fallback Option 2: Directly provide your API key here if Option 1 fails or for quick testing
# IMPORTANT: Replace 'YOUR_NEW_SECURE_API_KEY_HERE' with your actual, new API key.
# Keep this key confidential!
if not API_KEY:
    API_KEY = "AIzaSyAWKyx5YW-bbgUkwi6rjohVvq3lzTc8k-w" # <-- **REPLACE THIS WITH YOUR NEW KEY**

if not API_KEY or API_KEY == "YOUR_NEW_SECURE_API_KEY_HERE":
    print("\nERROR: Please replace 'YOUR_NEW_SECURE_API_KEY_HERE' in this script with your actual Gemini API key.")
    print("Remember to revoke any old, publicly shared keys and generate a new one.")
else:
    try:
        genai.configure(api_key=API_KEY)
        print("\nAvailable Gemini Models (supporting generateContent):")
        found_model = False
        for m in genai.list_models():
            if "generateContent" in m.supported_generation_methods:
                print(f"- {m.name} (DisplayName: {m.display_name})")
                found_model = True

        if not found_model:
            print("No models supporting 'generateContent' were found with your API key.")
            print("Please ensure your API key is correct and has access to Gemini models.")
    except Exception as e:
        print(f"\nAn error occurred during API configuration or model listing: {e}")
        print("Please double-check your API key and internet connection.")