# chatbot/urls.py
from django.urls import path
from . import views

app_name = 'chatbot' # Recommended for namespacing

urlpatterns = [
    path('ai-counselor/', views.ai_counselor_interface, name='ai_counselor_interface'),
    path('ai-counselor/chat/', views.chat_with_ai_counselor, name='chat_with_ai_counselor'),
]