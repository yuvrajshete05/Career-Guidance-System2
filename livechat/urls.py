# livechat/urls.py
from django.urls import path
from . import views

app_name = 'livechat'

urlpatterns = [
    path('request/', views.user_chat_request, name='user_chat_request'),
    path('room/<str:room_name>/', views.chat_room, name='chat_room'),
    path('counselor/dashboard/', views.counselor_dashboard, name='counselor_dashboard'),
    path('counselor/join/<int:session_id>/', views.counselor_join_session, name='counselor_join_session'),

     # Scheduling URLs
    path('counselor/add-availability/', views.counselor_add_availability, name='counselor_add_availability'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('my-appointments/', views.my_appointments, name='my_appointments'),
]