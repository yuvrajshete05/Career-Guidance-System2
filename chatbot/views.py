# chatbot/views.py
import openai
import os
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt # Be careful with this in production!
from django.contrib.auth.decorators import login_required
from .models import Conversation

# Ensure your OpenAI API key is loaded
openai.api_key = settings.OPENAI_API_KEY

# @csrf_exempt is used here for simplicity during development.
# In a production environment, you should use proper CSRF tokens for POST requests,
# especially when using JavaScript Fetch API.
# If your frontend is Django templates with proper CSRF token inclusion,
# you might not need this decorator if you handle the token correctly.
@csrf_exempt
@login_required # Ensure only logged-in users can chat
def chat_with_ai_counselor(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        if not user_message:
            return JsonResponse({'error': 'No message provided'}, status=400)

        user = request.user # The authenticated user

        # Retrieve historical conversation for this user
        conversation_history = Conversation.objects.filter(user=user).order_by('timestamp')

        messages = [
            {"role": "system", "content": "You are a helpful and empathetic career guidance counselor. Provide personalized, actionable, and encouraging advice based on the user's queries. Keep your responses concise yet informative."}
        ]

        # Add past conversation to context (last N messages to stay within token limits)
        # Adjust the number (e.g., 10) based on how much history you want to send
        for entry in conversation_history.all():
            messages.append({"role": entry.role, "content": entry.message})

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        try:
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo", # You can use "gpt-4" if you have access and need higher quality
                messages=messages,
                max_tokens=800, # Max tokens for the AI's response (adjust as needed)
                temperature=0.7, # Creativity: 0.0 (factual) to 1.0 (creative)
            )
            ai_response_content = response.choices[0].message['content'].strip()

            # Save current interaction to history
            Conversation.objects.create(user=user, role='user', message=user_message)
            Conversation.objects.create(user=user, role='assistant', message=ai_response_content)

            return JsonResponse({'response': ai_response_content})

        except openai.error.OpenAIError as e:
            # Specific OpenAI API errors
            print(f"OpenAI API Error: {e}")
            return JsonResponse({'error': f'OpenAI API error: {e}'}, status=500)
        except Exception as e:
            # Catch any other unexpected errors
            print(f"Unexpected error: {e}")
            return JsonResponse({'error': 'An unexpected error occurred. Please try again later.'}, status=500)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

# A simple view to render the chat interface
from django.shortcuts import render

@login_required
def ai_counselor_interface(request):
    # You could optionally load initial conversation history here
    # for display on page load, or fetch it via JS.
    return render(request, 'chatbot/ai_counselor_interface.html', {})