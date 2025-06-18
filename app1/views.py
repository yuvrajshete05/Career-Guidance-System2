# from django.shortcuts import render, redirect
# from django.http import HttpResponse, JsonResponse
# from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User # Corrected import for User
# from django.contrib import messages # Corrected import for messages
# from django.db.models import Q # For complex queries in search_view
# from django.views.decorators.csrf import csrf_exempt # Corrected import for csrf_exempt
# from django.conf import settings

# # Import external libraries
# import wikipedia # Make sure you have 'wikipedia' library installed (pip install wikipedia)
# import joblib    # Make sure you have 'scikit-learn' or 'joblib' installed (pip install scikit-learn)
# import re
# import os

# # Import Django settings
# from django.conf import settings # Import settings to access GEMINI_API_KEY

# # Import for Gemini API
# import google.generativeai as genai # Make sure you have 'google-generativeai' installed (pip install google-generativeai)

# # --- MODELS IMPORT (UNCOMMENT AND VERIFY) ---
# # You had these models imported, ensure they exist in app1/models.py
# # If they are correctly defined in app1/models.py, uncomment these lines.
# # from .models import Career, Skill, Course, Contact
# # If your Contact model is in loginform/models.py, import it like:
# # from loginform.models import Contact


# # --- Authentication Views ---

# def SignupPage(request):
#     if request.method == 'POST':
#         uname = request.POST.get('username')
#         email = request.POST.get('email')
#         pass1 = request.POST.get('password1')
#         pass2 = request.POST.get('password2')

#         if pass1 != pass2:
#             messages.error(request, "Passwords do not match.")
#             return render(request, 'signup.html', {'message': "Passwords do not match."})
#         if User.objects.filter(username=uname).exists():
#             messages.error(request, "Username already exists.")
#             return render(request, 'signup.html', {'message': "Username already exists."})
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already registered.")
#             return render(request, 'signup.html', {'message': "Email already registered."})

#         user = User.objects.create_user(username=uname, email=email, password=pass1)
#         user.save()
#         messages.success(request, "Account created successfully! Please login.")
#         return redirect('login')

#     return render(request, 'signup.html')

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('pass') # Note: your field name is 'pass' not 'password'

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             messages.success(request, f"Welcome, {username}!")
#             return redirect('home')
#         else:
#             messages.error(request, "Invalid username or password.")

#     return render(request, 'login.html')

# def LogoutPage(request):
#     logout(request)
#     messages.info(request, "You have been logged out.")
#     return redirect('login')


# # --- Core Application Views ---

# def HomePage(request):
#     return render(request, 'home.html')

# def career_form_view(request):
#     """
#     Renders the career recommendation form (career_form2.html).
#     This is what opens when 'Get Started!' is clicked.
#     """
#     return render(request, 'career_form2.html')

# @csrf_exempt # Use this decorator for testing. FOR PRODUCTION: Ensure {% csrf_token %} is in your form and remove this decorator!
# def career_recommendation(request):
#     if request.method == 'POST':
#         full_name = request.POST.get('name')
#         gender = request.POST.get('gender')
#         age = request.POST.get('age')
#         ug_course = request.POST.get('course')
#         ug_specialization = request.POST.get('ug_specialization')
#         cgpa = request.POST.get('cgpa')
#         interests = request.POST.get('interests')
#         skills = request.POST.get('skills')
#         certifications = request.POST.get('certifications')
#         is_working = request.POST.get('working')
#         current_job_title = request.POST.get('job_title')
#         masters_field = request.POST.get('masters_field', 'N/A')

#         prompt = (
#             f"Student Details:\n"
#             f"Name: {full_name}\n"
#             f"Gender: {gender}\n"
#             f"Age: {age}\n"
#             f"Undergraduate: {ug_course} in {ug_specialization}\n"
#             f"CGPA: {cgpa}\n"
#             f"Interests: {interests}\n"
#             f"Skills: {skills}\n"
#             f"Certifications: {certifications}\n"
#             f"Currently Working: {is_working}\n"
#             f"Job Title: {current_job_title}\n"
#             f"Master’s Degree Field: {masters_field}\n\n"
#             f"Based on these details, suggest the top 3 most suitable career paths and explain why each fits the candidate."
#         )

#         try:
#             if settings.DEBUG:
#                 print(f"DEBUG: Attempting to use FULL GEMINI_API_KEY: {settings.GEMINI_API_KEY}")
#             else:
#                 # Truncated print for non-debug mode (though not strictly needed in this simplified example)
#                 print(f"DEBUG: Attempting to use GEMINI_API_KEY: {settings.GEMINI_API_KEY[:5]}...{settings.GEMINI_API_KEY[-5:]}")

#             genai.configure(api_key=settings.GEMINI_API_KEY)
#             model = genai.GenerativeModel("gemini-1.5-flash")
#             response = model.generate_content(prompt)

#             if response.text:
#                 ai_reply = response.text.strip()
#                 return render(request, 'career_result2.html', {'recommendation': ai_reply})
#             else:
#                 messages.error(request, 'No text content in AI response. It might have been blocked by safety settings or be an empty response.')
#                 return render(request, 'career_form2.html', {'error_message': 'Could not get a recommendation. Please try again.'})

#         except Exception as e:
#             print(f"Error calling Gemini API: {e}")
#             messages.error(request, f"Failed to get recommendation: {str(e)}")
#             return render(request, 'career_form2.html', {'error_message': f"Failed to get recommendation: {str(e)}"})

#     return redirect('career_form')


# # --- Other Application Views ---

# def about_view(request):
#     return render(request, 'about.html')

# def assessment_view(request):
#     return render(request, 'assessment.html')

# def profile_view(request):
#     return render(request, 'profile.html')

# def contact_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')
#         # Uncomment and ensure Contact model is correctly imported and defined.
#         # from .models import Contact
#         # Contact.objects.create(name=name, email=email, message=message)
#         messages.success(request, "Your message has been sent!")
#         # CHANGE: Render the contact.html page itself instead of redirecting
#         return render(request, 'contact.html') # Render contact.html with the message

#     return render(request, 'contact.html')

# def search_view(request):
#     query = request.GET.get('query', '').strip()

#     # Uncomment and ensure Career, Skill, Course models are correctly imported and defined.
#     # from .models import Career, Skill, Course
#     # careers = Career.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
#     # skills = Skill.objects.filter(Q(name__icontains=query) | Q(detail__icontains=query))
#     # courses = Course.objects.filter(Q(name__icontains=query) | Q(overview__icontains=query))

#     # Mock data if models are not yet defined (remove this if you uncomment models above)
#     careers = []
#     skills = []
#     courses = []
#     if query:
#         if "data scientist" in query.lower():
#             careers.append({'title': 'Data Scientist', 'description': 'Analyzes large datasets.'})
#         if "python" in query.lower():
#             skills.append({'name': 'Python', 'detail': 'Programming language.'})
#         if "machine learning" in query.lower():
#             courses.append({'name': 'Machine Learning Fundamentals', 'overview': 'Intro to ML algorithms.'})


#     wiki_summary = None
#     wiki_url = None

#     if query:
#         try:
#             wiki_summary = wikipedia.summary(query, sentences=3, auto_suggest=True, redirect=True)
#             wiki_page = wikipedia.page(query)
#             wiki_url = wiki_page.url
#         except wikipedia.exceptions.DisambiguationError as e:
#             wiki_summary = f"Your search term is ambiguous. Possible options: {', '.join(e.options[:5])}"
#         except wikipedia.exceptions.PageError:
#             wiki_summary = "No Wikipedia page found for your query."
#         except Exception as e:
#             wiki_summary = f"Error fetching Wikipedia data: {e}"

#     context = {
#         'query': query,
#         'careers': careers,
#         'skills': skills,
#         'courses': courses,
#         'wiki_summary': wiki_summary,
#         'wiki_url': wiki_url,
#     }
#     return render(request, 'search_results.html', context)

# def thank_you(request):
#     return render(request, 'thankyou.html')

# # Placeholder for my_ai_view if you intend to use it separately
# # from .utils import get_gemini_key
# # def my_ai_view(request):
# #     key = get_gemini_key()
# #     # Use it to call Gemini API securely
# #     return HttpResponse(f"Gemini API key loaded: {key[:5]}...") # Just for testing key loading



import json # Make sure this import is at the top
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import wikipedia
import joblib
import re
import os

import google.generativeai as genai


# --- Authentication Views ---

def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html', {'message': "Passwords do not match."})
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html', {'message': "Username already exists."})
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'signup.html', {'message': "Email already registered."})

        user = User.objects.create_user(username=uname, email=email, password=pass1)
        user.save()
        messages.success(request, "Account created successfully! Please login.")
        return redirect('login')

    return render(request, 'signup.html')

def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pass')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome, {username}!")
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')

def LogoutPage(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


# --- Core Application Views ---

def HomePage(request):
    return render(request, 'home.html')

def career_form_view(request):
    """
    Renders the career recommendation form (career_form2.html).
    This is what opens when 'Get Started!' is clicked.
    """
    return render(request, 'career_form2.html')

@csrf_exempt
def career_recommendation(request):
    if request.method == 'POST':
        # Retrieve all form data
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        course = request.POST.get('course')
        ug_specialization = request.POST.get('ug_specialization')
        cgpa = request.POST.get('cgpa')
        interests = request.POST.get('interests')
        skills = request.POST.get('skills')
        certifications = request.POST.get('certifications')
        working = request.POST.get('working')
        job_title = request.POST.get('job_title')
        masters_field = request.POST.get('masters_field', 'N/A')

        # --- SIMPLIFIED AI Prompt: Only asks for recommendation text ---
        prompt = (
            f"Based on the following student details, suggest the top 3 most suitable career paths and explain why each fits the candidate.\n"
            f"Format your entire response as a JSON object with the following structure:\n"
            f'{{\n'
            f'  "recommendation_text": "Your detailed text recommendation here."\n'
            f'}}\n\n'
            f"DO NOT include any introductory or concluding text outside the JSON.\n\n"
            f"Student Details:\n"
            f"Name: {name}\n"
            f"Gender: {gender}\n"
            f"Age: {age}\n"
            f"Undergraduate: {course} in {ug_specialization}\n"
            f"CGPA: {cgpa}\n"
            f"Interests: {interests}\n"
            f"Skills: {skills}\n"
            f"Certifications: {certifications}\n"
            f"Currently Working: {working}\n"
            f"Job Title: {job_title}\n"
            f"Master’s Degree Field: {masters_field}\n"
        )
        # --- END OF SIMPLIFIED PROMPT ---

        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            recommendation_text = "No recommendation text provided."

            if response and response.text:
                try:
                    clean_text = response.text.strip()
                    # Clean the raw text to ensure it's valid JSON
                    if clean_text.startswith('```json'):
                        clean_text = clean_text[7:]
                    if clean_text.endswith('```'):
                        clean_text = clean_text[:-3]
                    ai_data = json.loads(clean_text)

                    recommendation_text = ai_data.get('recommendation_text', 'No recommendation text provided.')
                    # Removed parsing of graph/score data as per request.

                except json.JSONDecodeError as e:
                    print(f"ERROR: Could not decode JSON from Gemini API: {e}")
                    print(f"RAW AI Response: {response.text}")
                    recommendation_text = "Error: Could not parse AI recommendation. Please try again."
                    messages.error(request, "Failed to get structured recommendation from AI.")
            else:
                messages.error(request, "Empty or invalid response from AI.")

            # Prepare context for career_result2.html - ONLY include the requested data
            context = {
                'name': name,
                'gender': gender,
                'age': age,
                'course': course,
                'ug_specialization': ug_specialization,
                'cgpa': cgpa,
                'interests': interests,
                'skills': skills,
                'certifications': certifications,
                'working': working,
                'job_title': job_title,
                'masters_field': masters_field,
                'recommendation': recommendation_text,
                # Removed graph/score data from context as per user's request.
            }

            # --- RENDER THE TEMPLATE DIRECTLY ---
            return render(request, 'career_result2.html', context)

        except Exception as e:
            print(f"Error calling Gemini API: {type(e).__name__}, Message: {str(e)}")
            messages.error(request, f"Failed to get recommendation: {str(e)}")
            return render(request, 'career_form2.html', {'error_message': f"Failed to get recommendation: {str(e)}"})

    return redirect('career_form')


# --- Other Application Views ---

def dashboard_view(request):
    """
    Renders the main dashboard page.
    This view retrieves pre-processed data from the session for display.
    (Note: This view is kept for existing URL patterns but won't receive structured
    graph data from career_recommendation anymore.)
    """
    context = request.session.get('user_dashboard_data', None)

    if not context:
        messages.warning(request, "Please submit the career form to see your dashboard.")
        return redirect('career_form') # Redirect to form if no data in session

    return render(request, 'dashboard.html', context)


def about_view(request):
    return render(request, 'about.html')

def assessment_view(request):
    return render(request, 'assessment.html')

def profile_view(request):
    return render(request, 'profile.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        # Here you would typically save the contact form data to your database.
        # Example: Contact.objects.create(name=name, email=email, message=message)
        messages.success(request, "Your message has been sent!")
        return render(request, 'contact.html')

    return render(request, 'contact.html')

def search_view(request):
    query = request.GET.get('query', '').strip()
    careers = [] # Placeholder/mock data
    skills = []
    courses = []
    wiki_summary = None
    wiki_url = None

    if query:
        try:
            wiki_summary = wikipedia.summary(query, sentences=3, auto_suggest=True, redirect=True)
            wiki_page = wikipedia.page(query)
            wiki_url = wiki_page.url
        except wikipedia.exceptions.DisambiguationError as e:
            wiki_summary = f"Your search term is ambiguous. Possible options: {', '.join(e.options[:5])}"
        except wikipedia.exceptions.PageError:
            wiki_summary = "No Wikipedia page found for your query."
        except Exception as e:
            wiki_summary = f"Error fetching Wikipedia data: {e}"

    context = {
        'query': query,
        'careers': careers,
        'skills': skills,
        'courses': courses,
        'wiki_summary': wiki_summary,
        'wiki_url': wiki_url,
    }
    return render(request, 'search_results.html', context)

def thank_you(request):
    return render(request, 'thankyou.html')
