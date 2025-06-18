from django.urls import path
from .views import career_form, career_recommendation
from .views import dashboard_view

urlpatterns = [
    path('', career_form, name='career_form'),
    path('recommend/', career_recommendation, name='career_recommend'),
    path('dashboard/', dashboard_view, name='dashboard'),
]
