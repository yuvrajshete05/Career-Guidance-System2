# from django.contrib import admin
# from django.urls import path
# from app1 import views



# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.SignupPage, name='signup'),
#     path('login/', views.LoginPage, name='login'),     # Make sure this is here
#     path('home/', views.HomePage, name='home'),
#     path('logout/', views.LogoutPage, name='logout'),   # This handles logout

#     path('assessment/', views.assessment_view, name='assessment'),
#     path('profile/', views.profile_view, name='profile'),
# ]






# from django.contrib import admin
# from django.urls import path
# from app1 import views

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', views.SignupPage, name='signup'),
#     path('login/', views.LoginPage, name='login'),
#     path('home/', views.HomePage, name='home'),
#     path('logout/', views.LogoutPage, name='logout'),
#     path('assessment/', views.assessment_view, name='assessment'),
#     path('profile/', views.profile_view, name='profile'),
# ]


from django.contrib import admin
from django.urls import path
from app1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('home/', views.HomePage, name='home'),
    path('logout/', views.LogoutPage, name='logout'),
    path('assessment/', views.assessment_view, name='assessment'),
    path('profile/', views.profile_view, name='profile'),
    path('search/', views.search_view, name='search'),  # Only one search path here
    path('contact/', views.contact_view, name='contact'),
    path('submit/', views.submit_form, name='submit'),
    path('about/', views.about_view, name='about'), 
       

]
