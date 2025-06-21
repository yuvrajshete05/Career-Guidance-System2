# # loginform/urls.py

# from django.contrib import admin
# from django.urls import path, include
# from app1 import views # Ensure views from app1 are imported

# urlpatterns = [
#     # Admin site URL
#     path('admin/', admin.site.urls),

#     # Main Application URLs
#     # This sets the root URL ('') to your SignupPage view.
#     path('', views.SignupPage, name='signup'),

#     # URL for the career recommendation form page, opened by "Get Started!"
#     path('career_form/', views.career_form_view, name='career_form'),

#     # URL for processing the career recommendation form (from career_form2.html)
#     # This will now render career_results_dashboard.html, as per our recent discussion.
#     path('recommend/', views.career_recommendation, name='career_recommend'),

#     # --- CRITICAL ADDITION: URL for the Dashboard ---
#     # This path is essential for the dashboard_view to be accessible if you decide
#     # to redirect to it later, or navigate to it directly.
#     path('dashboard/', views.dashboard_view, name='dashboard'),


#     # Other specific URLs for your application, handled by views in 'app1'
#     path('login/', views.login_view, name='login'),
#     path('home/', views.HomePage, name='home'),
#     path('logout/', views.LogoutPage, name='logout'),
#     path('assessment/', views.assessment_view, name='assessment'),
#     path('profile/', views.profile_view, name='profile'),
#     path('search/', views.search_view, name='search'),
#     path('contact/', views.contact_view, name='contact'),
#     path('about/', views.about_view, name='about'),
#     path('thankyou/', views.thank_you, name='thankyou'),

#     # --- NEW: URL for dynamic tests ---
#     # This pattern captures the test_type (e.g., 'computer_science', 'coding')
#     # and passes it as an argument to the generate_test view.
#     path('test/<str:test_type>/', views.generate_test, name='generate_test'),
#     path('resume-builder/', views.resume_builder_view, name='resume_builder'),

#     # --- IMPORTANT CHANGE: Django's built-in authentication URLs ---
#     # It's best practice to include Django's auth URLs under a prefix like 'accounts/'
#     # to avoid conflicts with your root URL and other custom URLs.
#     path('/', include('django.contrib.auth.urls')),
#     path('livechat/', views.live_chat_view, name='live_chat'),

# ]



# from django.contrib import admin
# from django.urls import path, include
# from app1 import views # Ensure views from app1 are imported

# urlpatterns = [
#     # Admin site URL
#     path('admin/', admin.site.urls),

#     # Main Application URLs
#     # This sets the root URL ('') to your SignupPage view.
#     path('', views.SignupPage, name='signup'),

#     # URL for the career recommendation form page, opened by "Get Started!"
#     path('career_form/', views.career_form_view, name='career_form'),

#     # URL for processing the career recommendation form (from career_form2.html)
#     # This will now render career_result2.html directly, as per your last request.
#     path('recommend/', views.career_recommendation, name='career_recommend'),

#     # --- CRITICAL ADDITION: URL for the Dashboard ---
#     # This path is essential for the dashboard_view to be accessible if you decide
#     # to redirect to it later, or navigate to it directly.
#     path('dashboard/', views.dashboard_view, name='dashboard'),


#     # Other specific URLs for your application, handled by views in 'app1'
#     path('login/', views.login_view, name='login'),
#     path('home/', views.HomePage, name='home'),
#     path('logout/', views.LogoutPage, name='logout'),
#     path('assessment/', views.assessment_view, name='assessment'),
#     path('profile/', views.profile_view, name='profile'),
#     path('search/', views.search_view, name='search'),
#     path('contact/', views.contact_view, name='contact'),
#     path('about/', views.about_view, name='about'),
#     path('thankyou/', views.thank_you, name='thankyou'),
    

#     # --- IMPORTANT CHANGE: Django's built-in authentication URLs ---
#     # It's best practice to include Django's auth URLs under a prefix like 'accounts/'
#     # to avoid conflicts with your root URL and other custom URLs.
#     path('accounts/', include('django.contrib.auth.urls')),
# ]

from django.contrib import admin
from django.urls import path, include
from app1 import views


from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.SignupPage, name='signup'),
    path('career_form/', views.career_form_view, name='career_form'),
    path('recommend/', views.career_recommendation, name='career_recommend'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('assessment/', views.assessment_view, name='assessment'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.search_view, name='search'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('thankyou/', views.thank_you, name='thankyou'),

    # ✅ Add this for quiz/test generation URLs
    path('generate/<str:test_type>/', views.generate_test, name='generate_test'),

    path('', include('django.contrib.auth.urls')),
    path('resume/', views.resume_builder_view, name='resume_builder'),
    path('livechat/', views.live_chat_view, name='live_chat'),



    path('career_result/', views.career_result_view, name='career_result'),




]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)