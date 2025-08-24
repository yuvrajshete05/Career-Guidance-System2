


# # C:\...\loginform\urls.py

# from django.contrib import admin
# from django.urls import path, include
# from app1 import views
# from django.conf import settings
# from django.conf.urls.static import static

# urlpatterns = [
#     # Admin site
#     path('admin/', admin.site.urls),

#     # User Authentication & Core pages
#     path('', views.SignupPage, name='signup'),
#     path('login/', views.login_view, name='login'),
#     path('home/', views.HomePage, name='home'),
#     path('logout/', views.LogoutPage, name='logout'),
    
#     # Career Recommendation
#     path('career_form/', views.career_form_view, name='career_form'),
#     path('recommend/', views.career_recommendation, name='career_recommend'),
#     path('career_result/', views.career_result_view, name='career_result'),
    
#     # Assessments & Tests
#     path('assessment/', views.assessment_view, name='assessment'),
#     path('generate/<str:test_type>/', views.generate_test, name='generate_test'),
    
#     # AI-powered tools
#     path('live_chat/', views.live_chat_view, name='live_chat'),
#     path('startchat/', views.ai_career_assistant, name='start_chat'),
#     path('resume/', views.resume_builder_view, name='resume_builder'),
    
#     # User-related pages
#     path('dashboard/', views.dashboard_view, name='dashboard'),
#     path('profile/', views.profile_view, name='profile'),
    
#     # Informational pages
#     path('search/', views.search_view, name='search'),
#     path('contact/', views.contact_view, name='contact'),
#     path('about/', views.about_view, name='about'),
#     path('thankyou/', views.thank_you, name='thankyou'),
    
#     # Default Django Auth URLs
#     path('', include('django.contrib.auth.urls')),

#     path('tests/', views.company_tests_page, name='company_tests_page'),
#     path('tests/<slug:company_slug>/', views.company_details_page, name='company_details'),
#     path('api/tests/<slug:company_slug>/', views.get_company_details_api, name='get_company_details_api'),

    
    
# ]

# if settings.DEBUG:
#     from django.conf.urls.static import static
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# loginform/urls.py

from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app1 import views  # Make sure you're importing views from your app
from django.contrib import admin

urlpatterns = [
    # 1. Admin and Core Application URLs
    path('admin/', admin.site.urls),
    path('', views.SignupPage, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # 2. Most Specific Dynamic URLs (must come before any generic patterns)
    path('tests/', views.company_tests_page, name='company_tests_page'),
    path('tests/<slug:company_slug>/', views.company_details_page, name='company_details'),
    
    # 3. Other Application URLs
    path('career_form/', views.career_form_view, name='career_form'),
    path('recommend/', views.career_recommendation, name='career_recommend'),
    path('career_result/', views.career_result_view, name='career_result'),
    path('assessment/', views.assessment_view, name='assessment'),
    path('generate/<str:test_type>/', views.generate_test, name='generate_test'),
    path('live_chat/', views.live_chat_view, name='live_chat'),
    path('startchat/', views.ai_career_assistant, name='start_chat'),
    path('resume/', views.resume_builder_view, name='resume_builder'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.search_view, name='search'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('thankyou/', views.thank_you, name='thankyou'),
    
    # 4. Django's built-in authentication URLs
    #    Give this a specific prefix like 'accounts/' to avoid conflicts
    path('accounts/', include('django.contrib.auth.urls')),

    path('api/company_info/<slug:company_slug>/', views.get_company_info_api, name='api_company_info'),

    # The existing view that renders the company details page
    path('tests/<slug:company_slug>/', views.company_details_page, name='company_details'),

    path('jobs/', views.get_realtime_jobs, name='get_realtime_jobs'),
]

# 5. Static and Media File serving (MUST be at the very end)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)