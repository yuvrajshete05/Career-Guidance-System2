from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.SignupPage, name='signup'),
    path('login/', views.login_view, name='login'),  # use the login_view that handles saving
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('assessment/', views.assessment_view, name='assessment'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.search_view, name='search'),
    path('contact/', views.contact_view, name='contact'),
    path('submit/', views.submit_form, name='submit'),
    path('about/', views.about_view, name='about'), 
    path('thankyou/', views.thank_you, name='thankyou'),
    path('login/', views.login_view, name='login'), 
]
