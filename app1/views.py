# from django.shortcuts import render, redirect,HttpResponse
# from django.contrib.auth import logout
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate,login

# def HomePage(request):
#     return render(request, 'home.html')

# from django.contrib.auth.models import User
# from django.shortcuts import render, redirect
# from django.http import HttpResponse

# def SignupPage(request):
#     if request.method == 'POST':
#         uname = request.POST.get('username')
#         email = request.POST.get('email')
#         pass1 = request.POST.get('password1')
#         pass2 = request.POST.get('password2')

#         if pass1 != pass2:
#             return HttpResponse("Your password and Confirm password are not same !!")

#         if User.objects.filter(username=uname).exists():
#             return HttpResponse("Username already exists. Please choose a different one.")

#         if User.objects.filter(email=email).exists():
#             return HttpResponse("Email already registered. Try logging in or use another email.")

  
#         my_user = User.objects.create_user(username=uname, email=email, password=pass1)
#         my_user.save()
#         return redirect('login')

#     return render(request, 'signup.html')





# def LoginPage(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         pass1=request.POST.get('pass')
#         user=authenticate(request,username=username,password=pass1)
#         if user is not None:
#             login(request,user)
#             return redirect('home')
#         else:
#             return HttpResponse("Username or Password is incorrect!!!")

#     return render(request,'login.html')


# def LogoutPage(request):
#     logout(request)
#     return redirect('login')


# def assessment_view(request):
#     return render(request, 'assessment.html')



from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Career, Skill, Course
from django.db.models import Q
import wikipedia
import joblib 
import os
from django.conf import settings


# Home Page
def HomePage(request):
    return render(request, 'home.html')

# Signup Page
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Passwords do not match.")
        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists.")
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered.")

        user = User.objects.create_user(username=uname, email=email, password=pass1)
        user.save()
        return redirect('login')

    return render(request, 'signup.html')

# Login Page
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse("Invalid username or password.")

    return render(request, 'login.html')

# Logout
def LogoutPage(request):
    logout(request)
    return redirect('login')

def about_view(request):
    return render(request, 'about.html')


# Assessment Page
def assessment_view(request):
    return render(request, 'assessment.html')

# Profile Page
def profile_view(request):
    return render(request, 'profile.html')

# Contact Page
def contact_view(request):
    return render(request, 'contact.html')

# Chatbot-like Search View
def search_view(request):
    query = request.GET.get('query', '').strip()
    
    careers = Career.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    skills = Skill.objects.filter(Q(name__icontains=query) | Q(detail__icontains=query))
    courses = Course.objects.filter(Q(name__icontains=query) | Q(overview__icontains=query))
    
    wiki_summary = None
    wiki_url = None
    
    if query:
        try:
            # Get the summary of the page (limit sentences)
            wiki_summary = wikipedia.summary(query, sentences=3, auto_suggest=True, redirect=True)
            # Get the full URL
            wiki_page = wikipedia.page(query)
            wiki_url = wiki_page.url
        except wikipedia.exceptions.DisambiguationError as e:
            wiki_summary = f"Your search term is ambiguous. Possible options: {e.options[:5]}"
        except wikipedia.exceptions.PageError:
            wiki_summary = "No Wikipedia page found for your query."
        except Exception as e:
            wiki_summary = "Error fetching Wikipedia data."

    context = {
        'query': query,
        'careers': careers,
        'skills': skills,
        'courses': courses,
        'wiki_summary': wiki_summary,
        'wiki_url': wiki_url,
    }
    return render(request, 'search_results.html', context)


# def submit_view(request):
#     if request.method == 'POST':
#         # handle form submission / prediction here
#         ...
#         return render(request, 'result.html', context)
#     else:
#         # optionally handle GET or redirect
#         return redirect('home')  # or some other pagedef submit_form(request):def submit_form(request):


# def submit_form(request):
#     if request.method == "POST":
#         # Get and normalize all inputs
#         def normalize(text):
#             return text.strip().lower() if text else ""

#         name = normalize(request.POST.get('name'))
#         gender = normalize(request.POST.get('gender'))
#         age = normalize(request.POST.get('age'))
#         course = normalize(request.POST.get('course'))
#         ug_specialization = normalize(request.POST.get('ug_specialization'))
#         cgpa = normalize(request.POST.get('cgpa'))
#         interest = normalize(request.POST.get('interest'))
#         interests = normalize(request.POST.get('interests'))
#         skills = normalize(request.POST.get('skills'))
#         certifications = normalize(request.POST.get('certifications'))
#         working = normalize(request.POST.get('working'))
#         job_title = normalize(request.POST.get('job_title'))
#         masters_field = normalize(request.POST.get('masters_field'))

#         # Combine and split into individual words
#         combined_text = f"{course} {ug_specialization} {interest} {interests} {skills} {certifications} {job_title} {masters_field}"
#         words = set(combined_text.lower().split())

#         print("Combined Text:", combined_text)
#         print("Extracted Words:", words)

#         career_keywords = {
#             "Software Engineer": {"programming", "computer", "technology", "python", "java", "developer"},
#             "Graphic Designer": {"drawing", "design", "graphic", "photoshop", "illustrator"},
#             "Marketing Manager": {"communication", "business", "marketing", "sales", "commerce"},
#             "Doctor": {"biology", "medicine", "surgery", "anatomy", "hospital"},
#             "Engineer": {"physics", "maths", "engineering", "mechanical", "civil"},
#             "Data Scientist": {"data", "machine", "learning", "ai", "analytics", "statistics"},
#         }

#         max_score = 0
#         predicted_career = "General Career Advisor"

#         for career, keywords in career_keywords.items():
#             score = len(words.intersection(keywords))
#             print(f"Matching with {career}: {score}")
#             if score > max_score:
#                 max_score = score
#                 predicted_career = career

#         max_possible = len(career_keywords[predicted_career])
#         accuracy = int((max_score / max_possible) * 100) if max_possible else 0

#         context = {
#             'name': name,
#             'gender': gender,
#             'age': age,
#             'course': course,
#             'ug_specialization': ug_specialization,
#             'cgpa': cgpa,
#             'interest': interest,
#             'interests': interests,
#             'skills': skills,
#             'certifications': certifications,
#             'working': working,
#             'job_title': job_title,
#             'masters_field': masters_field,
#             'career': predicted_career,
#             'accuracy': f"{accuracy}%"
#         }

#         return render(request, 'result.html', context)

#     return render(request, 'home.html')

from django.shortcuts import render
import re

def submit_form(request):
    if request.method == "POST":
        # Get and normalize user input
        name = request.POST.get('name', '').strip()
        gender = request.POST.get('gender', '').strip()
        age = request.POST.get('age', '').strip()
        course = request.POST.get('course', '').strip()
        ug_specialization = request.POST.get('ug_specialization', '').strip()
        cgpa = request.POST.get('cgpa', '').strip()
        interest = request.POST.get('interest', '').strip()
        interests = request.POST.get('interests', '').strip()
        skills = request.POST.get('skills', '').strip()
        certifications = request.POST.get('certifications', '').strip()
        working = request.POST.get('working', '').strip()
        job_title = request.POST.get('job_title', '').strip()
        masters_field = request.POST.get('masters_field', '').strip()

        # Combine and clean text input for keyword matching
        combined_text = f"{course} {ug_specialization} {interest} {interests} {skills} {certifications} {job_title} {masters_field}"
        cleaned_text = re.sub(r'[^\w\s]', '', combined_text.lower())  # remove punctuation & lowercase
        words = set(cleaned_text.split())

        # Career keyword definitions
        career_keywords = {
            "Software Engineer": {"programming", "computer", "technology", "python", "java", "c++", "development", "software", "developer"},
            "Graphic Designer": {"drawing", "design", "graphic", "photoshop", "illustrator", "creativity", "adobe"},
            "Marketing Manager": {"communication", "business", "commerce", "marketing", "branding", "sales", "strategy"},
            "Doctor": {"biology", "medicine", "doctor", "clinical", "hospital", "healthcare"},
            "Engineer": {"physics", "math", "engineering", "mechanical", "civil", "electrical"},
            "Data Scientist": {"data", "machine", "learning", "ai", "analytics", "statistics", "python", "modeling"},
        }

        # Career prediction logic
        predicted_career = "General Career Advisor"
        max_match = 0
        matched_words = set()

        for career, keywords in career_keywords.items():
            match = words.intersection(keywords)
            if len(match) > max_match:
                predicted_career = career
                max_match = len(match)
                matched_words = match

        # Accuracy calculation
        if max_match > 0:
            accuracy = round((max_match / len(career_keywords[predicted_career])) * 100)
        else:
            predicted_career = "General Career Advisor"
            accuracy = 33

        # Render result
        context = {
            'name': name,
            'gender': gender,
            'age': age,
            'course': course,
            'ug_specialization': ug_specialization,
            'cgpa': cgpa,
            'interest': interest,
            'interests': interests,
            'skills': skills,
            'certifications': certifications,
            'working': working,
            'job_title': job_title,
            'masters_field': masters_field,
            'career': predicted_career,
            'accuracy': accuracy,
            'matched_words': matched_words,
        }

        return render(request, 'result.html', context)

    return render(request, 'home.html')



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactMessage

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Save to database
        ContactMessage.objects.create(name=name, email=email, message=message)

        messages.success(request, 'Your data was sent successfully!')
        return redirect('contact')

    return render(request, 'contact.html')
