from django.contrib import admin
from django.urls import path, include
from app1 import views # Ensure views from app1 are imported

urlpatterns = [
    # Admin site URL
    path('admin/', admin.site.urls),

    # Main Application URLs
    # This sets the root URL ('') to your SignupPage view.
    path('', views.SignupPage, name='signup'),

    # URL for the career recommendation form page, opened by "Get Started!"
    path('career_form/', views.career_form_view, name='career_form'),

    # URL for processing the career recommendation form (from career_form2.html)
    # This will now render career_result2.html directly, as per your last request.
    path('recommend/', views.career_recommendation, name='career_recommend'),

    # --- CRITICAL ADDITION: URL for the Dashboard ---
    # This path is essential for the dashboard_view to be accessible if you decide
    # to redirect to it later, or navigate to it directly.
    path('dashboard/', views.dashboard_view, name='dashboard'),


    # Other specific URLs for your application, handled by views in 'app1'
    path('login/', views.login_view, name='login'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('assessment/', views.assessment_view, name='assessment'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.search_view, name='search'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('thankyou/', views.thank_you, name='thankyou'),
    

    # --- IMPORTANT CHANGE: Django's built-in authentication URLs ---
    # It's best practice to include Django's auth URLs under a prefix like 'accounts/'
    # to avoid conflicts with your root URL and other custom URLs.
    path('accounts/', include('django.contrib.auth.urls')),
]
