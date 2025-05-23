from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),     # Make sure this is here
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),   # This handles logout
]
