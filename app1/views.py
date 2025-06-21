
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

#=======================================================================================================================================================

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

#=======================================================================================================================================================

def LogoutPage(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


#=======================================================================================================================================================

# --- Core Application Views ---

def HomePage(request):
    return render(request, 'home.html')

#=======================================================================================================================================================

def career_form_view(request):
    """
    Renders the career recommendation form (career_form2.html).
    This is what opens when 'Get Started!' is clicked.
    """
    return render(request, 'career_form2.html')

#=======================================================================================================================================================


from django.contrib.auth.decorators import login_required
@csrf_exempt # Consider removing this if using Django's {% csrf_token %} in your form
def career_recommendation(request):
    if request.method == 'POST':
        # Retrieve all form data
        # Using .get() with a default value is good practice for robustness
        name = request.POST.get('name', 'N/A')
        gender = request.POST.get('gender', 'N/A')
        age = request.POST.get('age', 'N/A')
        course = request.POST.get('course', 'N/A')
        ug_specialization = request.POST.get('ug_specialization', 'N/A')
        cgpa = request.POST.get('cgpa', 'N/A')
        interests = request.POST.get('interests', 'N/A')
        skills = request.POST.get('skills', 'N/A')
        certifications = request.POST.get('certifications', 'N/A')
        working = request.POST.get('working', 'No') # Default to 'No' if not provided
        job_title = request.POST.get('job_title', 'N/A')
        masters_field = request.POST.get('masters_field', 'N/A')

        # Constructing the prompt for Gemini API
        prompt = (
            f"Based on the following student details, suggest the top 3 most suitable career paths and explain why each fits the candidate.\n"
            f"Format your entire response strictly as a JSON object with the following structure:\n"
            f'{{\n'
            f'  "recommendation_text": "Your detailed text recommendation here."\n'
            f'}}\n\n'
            f"DO NOT include any introductory or concluding text outside the JSON. "
            f"Ensure the JSON is perfectly valid and unescaped.\n\n"
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

        recommendation_text = "No recommendation generated." # Default message

        try:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            model = genai.GenerativeModel("gemini-1.5-flash")
            response = model.generate_content(prompt)

            if response and response.text:
                try:
                    # Clean the raw text to ensure it's valid JSON
                    # Gemini often wraps JSON in triple backticks and 'json' tag
                    clean_text = response.text.strip()
                    if clean_text.startswith('```json'):
                        clean_text = clean_text[len('```json'):].strip()
                    if clean_text.endswith('```'):
                        clean_text = clean_text[:-len('```')].strip()

                    ai_data = json.loads(clean_text)
                    recommendation_text = ai_data.get('recommendation_text', recommendation_text)

                    # Optional: Log the successful AI response
                    print(f"Successfully received AI recommendation for {name}")

                except json.JSONDecodeError as e:
                    print(f"ERROR: Could not decode JSON from Gemini API: {e}")
                    print(f"RAW AI Response (problematic): {response.text}")
                    messages.error(request, "Failed to parse AI recommendation. Please try again or refine your input.")
                    recommendation_text = "Error: AI recommendation could not be processed."
                except Exception as e:
                    print(f"ERROR processing AI response: {type(e).__name__}, Message: {str(e)}")
                    messages.error(request, f"An unexpected error occurred with AI processing: {str(e)}")
                    recommendation_text = "An unexpected error occurred."
            else:
                messages.error(request, "Empty or invalid response from AI. Please try again.")

        except Exception as e:
            print(f"Error calling Gemini API: {type(e).__name__}, Message: {str(e)}")
            messages.error(request, f"Failed to get recommendation from AI: {str(e)}")
            # If AI call fails, render the form again with an error
            return render(request, 'career_form.html', {'error_message': f"Failed to get recommendation: {str(e)}"})

        # Prepare the data to be stored in the session for the dashboard
        # Only include data that you want to display on the dashboard
        user_dashboard_data = {
            'user_input': { # Group original input if needed
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
            },
            'ai_recommendation': recommendation_text,
            # Add any other derived data you want on the dashboard
        }

        # Store this data in the user's session
        request.session['user_dashboard_data'] = user_dashboard_data
        messages.success(request, "Your personalized career recommendation is ready!")

        # Redirect the user to the dashboard page
        return render(request, 'career_result2.html', {
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
        })

    # If the request method is GET, redirect to the career form
    return redirect('career_form')

#=======================================================================================================================================================


@login_required # Ensures only logged-in users can access the dashboard
def dashboard_view(request):
    """
    Renders the user's personalized dashboard page.
    It retrieves the career recommendation data from the session.
    """
    # Attempt to retrieve dashboard data from the session
    context = request.session.get('user_dashboard_data')

    if not context:
        # If no data is found, it means the career form hasn't been submitted
        # or the session expired/cleared.
        messages.info(request, "Welcome to your Dashboard! Please fill out the career recommendation form to see your personalized insights.")
        # Render the dashboard with a default message, or redirect to the form
        return render(request, 'dashboard.html', {'message': "No personalized data available yet. Please complete the career form."})
        # Alternatively, if you strictly require data to show the dashboard:
        # return redirect('career_form')

    # If context exists, render the dashboard with the stored data
    return render(request, 'dashboard.html', context)

#=======================================================================================================================================================



def about_view(request):
    return render(request, 'about.html')

#=======================================================================================================================================================

def assessment_view(request):
    return render(request, 'assessment.html')

#=======================================================================================================================================================

def profile_view(request):
    return render(request, 'profile.html')

#=======================================================================================================================================================

# def contact_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')
#         # Here you would typically save the contact form data to your database.
#         # Example: Contact.objects.create(name=name, email=email, message=message)
#         messages.success(request, "Your message has been sent!")
#         return render(request, 'contact.html')

#     return render(request, 'contact.html')



from django.contrib import messages
from django.shortcuts import render, redirect # Import redirect
from .models import ContactMessage # Import your ContactMessage model

def contact_view(request):
    # It's generally not recommended to clear messages this way.
    # Django's message system handles display and clearing automatically
    # once messages are consumed by a template. Removing this can avoid issues.
    # storage = get_messages(request)
    # list(storage) # This consumes and clears the messages

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # --- IMPORTANT: Save data to the database here ---
        try:
            ContactMessage.objects.create(
                name=name,
                email=email,
                message=message
            )
            messages.success(request, "Your message has been sent successfully!")
            # Redirect to the same contact page or a thank you page
            return redirect('contact') # Assuming 'contact' is the name of your URL pattern for this view.
                                     # Change 'contact' if your URL name is different.
        except Exception as e:
            messages.error(request, f"There was an error sending your message: {e}")
            # If there's an error, re-render the form to show the error
            return render(request, 'contact.html')


    return render(request, 'contact.html')
#=======================================================================================================================================================

def search_view(request):
    query = request.GET.get('query', '').strip()
    careers = [] # Placeholder/mock data
    skills = []
    courses = []
    wiki_summary = None
    wiki_url = None

    if query:
        # Attempt to get summary from Wikipedia first
        try:
            wiki_summary = wikipedia.summary(query, sentences=3, auto_suggest=True, redirect=True)
            wiki_page = wikipedia.page(query)
            wiki_url = wiki_page.url
        except wikipedia.exceptions.DisambiguationError as e:
            # Handle ambiguous queries by providing options
            wiki_summary = f"Your search term is ambiguous. Possible options: {', '.join(e.options[:5])}. Please refine your query for a more specific Wikipedia result."
            wiki_url = None # No specific URL if disambiguation occurs
        except wikipedia.exceptions.PageError:
            # No Wikipedia page found, fall back to Gemini
            wiki_summary = None # Clear Wikipedia summary to indicate failure
        except Exception as e:
            # General error with Wikipedia, fall back to Gemini
            print(f"Wikipedia error for query '{query}': {e}")
            wiki_summary = None # Clear Wikipedia summary to indicate failure
        
        # If Wikipedia failed to provide a summary, try Gemini as a fallback
        if wiki_summary is None or ("No Wikipedia page found" in wiki_summary) or ("Error fetching Wikipedia data" in wiki_summary):
            try:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                model = genai.GenerativeModel("gemini-1.5-flash") # Use gemini-1.5-flash for summaries
                gemini_summary_prompt = f"Provide a brief, concise summary of '{query}'. If it's a technical term, explain it simply. Limit to 3-4 sentences."
                
                gemini_response = model.generate_content(gemini_summary_prompt)
                
                if gemini_response and gemini_response.text:
                    gemini_text = gemini_response.text.strip()
                    # Clean up markdown if Gemini includes it
                    if gemini_text.startswith('```'):
                        gemini_text = gemini_text.lstrip('`').lstrip('json').strip()
                    if gemini_text.endswith('```'):
                        gemini_text = gemini_text.rstrip('`').strip()
                    
                    wiki_summary = f"Summary (via AI): {gemini_text}"
                    wiki_url = None # Gemini doesn't provide a direct URL, so clear any previous Wikipedia URL
                else:
                    wiki_summary = "Could not find information for your query."
                    wiki_url = None
            except Exception as e:
                print(f"Gemini API error for query '{query}': {e}")
                wiki_summary = "An error occurred while fetching information. Please try again later."
                wiki_url = None

    context = {
        'query': query,
        'careers': careers, # These are mock data, update your Django model/logic to populate these
        'skills': skills,   # if you want real search results for these categories.
        'courses': courses, # For now, they will remain empty unless your backend populates them.
        'wiki_summary': wiki_summary,
        'wiki_url': wiki_url,
    }
    return render(request, 'search_results.html', context)


#=======================================================================================================================================================

def thank_you(request):
    return render(request, 'thankyou.html')


#=======================================================================================================================================================


import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Import external libraries
import wikipedia
import re
import os

# Import for Gemini API
import google.generativeai as genai

# --- MODIFIED: AI-Generated Test View ---
@csrf_exempt
def generate_test(request, test_type): # test_type is correctly received here
    """
    Generates a dynamic test (MCQs or a coding challenge) using Gemini API.
    `test_type` can be 'computer_science', 'data_science', 'web_development', or 'coding'.
    """
    questions = []
    test_title = ""
    is_coding_challenge = False # Will be set to True only if it's the original coding challenge format

    # Initialize context with test_type immediately
    context = {
        'test_type': test_type, # <-- Add test_type to context at the start
        'test_title': test_title, # Will be updated later
        'is_coding_challenge': is_coding_challenge, # Will be updated later
        'error': None, # Initialize error to None
        'questions': [],
        'challenge_data': {},
    }

    gemini_prompt = ""
    if test_type == 'computer_science':
        test_title = "Computer Science Fundamentals Test"
        gemini_prompt = (
            "Generate 10 multiple-choice questions (MCQs) about fundamental Computer Science concepts (e.g., data structures, algorithms, operating systems, networking). "
            "For each question, provide 4 options (A, B, C, D) and indicate the correct answer. "
            "Format the output as a JSON array of objects, where each object has 'question', 'options' (a list of strings), and 'correct_answer' (the option letter, e.g., 'A').\n\n"
            "Example format: [\n"
            '   { "question": "What is encapsulation?", "options": ["A) Hiding data within a class", "B) Inheriting properties", "C) Overriding methods", "D) Creating multiple functions"], "correct_answer": "A" }\n'
            "]"
        )
    elif test_type == 'data_science':
        test_title = "Data Science & Machine Learning Test"
        gemini_prompt = (
            "Generate 10 multiple-choice questions (MCQs) about Data Science and Machine Learning concepts (e.g., supervised learning, regression, classification, data preprocessing). "
            "For each question, provide 4 options (A, B, C, D) and indicate the correct answer. "
            "Format the output as a JSON array of objects, where each object has 'question', 'options' (a list of strings), and 'correct_answer' (the option letter, e.g., 'A')."
        )
    elif test_type == 'web_development':
        test_title = "Web Development Fundamentals Test"
        gemini_prompt = (
            "Generate 10 multiple-choice questions (MCQs) about Web Development fundamentals (e.g., HTML, CSS, JavaScript, front-end vs back-end). "
            "For each question, provide 4 options (A, B, C, D) and indicate the correct answer. "
            "Format the output as a JSON array of objects, where each object has 'question', 'options' (a list of strings), and 'correct_answer' (the option letter, e.g., 'A')."
        )
    elif test_type == 'coding':
        test_title = "Coding Concepts Test (MCQs)"
        # is_coding_challenge remains False as it's now MCQs
        gemini_prompt = (
            "Generate 10 multiple-choice questions (MCQs) about fundamental coding concepts in Python (e.g., data types, control flow, functions, common built-in methods, basic algorithms, error handling). "
            "For each question, provide 4 options (A, B, C, D) and indicate the correct answer. "
            "Format the output as a JSON array of objects, where each object has 'question', 'options' (a list of strings), and 'correct_answer' (the option letter, e.g., 'A').\n\n"
            "Example format: [\n"
            '   { "question": "What is the output of `print(type([]))` in Python?", "options": ["A) <class \'list\'>", "B) <class \'array\'>", "C) <class \'tuple\'>", "D) <class \'object\'>"], "correct_answer": "A" }\n'
            "]"
        )
    else:
        messages.error(request, "Invalid test type specified.")
        # Ensure test_type is still in context even for invalid type
        context.update({'error': "Invalid test type specified."})
        return render(request, 'dynamic_test.html', context)

    # Update test_title and is_coding_challenge in context
    context.update({
        'test_title': test_title,
        'is_coding_challenge': is_coding_challenge, # This will now be False for 'coding' type
    })

    try:
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel("gemini-1.5-flash") # Or "gemini-pro" for higher quality if needed
        response = model.generate_content(gemini_prompt)

        if response and response.text:
            clean_text = response.text.strip()
            # Remove markdown code block fences if present
            if clean_text.startswith('```json'):
                clean_text = clean_text[len('```json'):]
            if clean_text.endswith('```'):
                clean_text = clean_text[:-len('```')]
            clean_text = clean_text.strip() # Strip any remaining whitespace

            if is_coding_challenge: # This block will only execute if is_coding_challenge was explicitly set to True
                coding_challenge_data = json.loads(clean_text)
                context['challenge_data'] = coding_challenge_data
            else: # This now covers all MCQ types, including the modified 'coding' type
                questions = json.loads(clean_text)
                context['questions'] = questions
            messages.success(request, f"Generated {test_title} successfully!")

        else:
            messages.error(request, "Empty or invalid response from AI for test generation.")
            context['error'] = "Failed to generate test questions."

    except json.JSONDecodeError as e:
        print(f"JSON Decode Error for test type {test_type}: {e}")
        print(f"RAW AI Response (problematic): {response.text}")
        messages.error(request, "Error parsing AI response for test. Please try again.")
        context['error'] = "Failed to parse AI test data."
    except Exception as e:
        print(f"Error generating test for {test_type}: {e}")
        messages.error(request, f"An error occurred while generating the test: {e}")
        context['error'] = "An unexpected error occurred."

    return render(request, 'dynamic_test.html', context)


#=======================================================================================================================================================

# app1/views.py

import json
import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ResumeInputForm
from .models import ResumeInput

# Your Gemini API Key has been updated here.
API_KEY = "AIzaSyAWKyx5YW-bbgUkwi6rjohVvq3lzTc8k-w" 

@login_required # Requires user to be logged in
def resume_builder_view(request):
    generated_resume_text = None
    form = ResumeInputForm() # Initialize form for GET or initial render

    if request.method == 'POST':
        form = ResumeInputForm(request.POST)
        if form.is_valid():
            resume_data = form.save(commit=False)
            resume_data.user = request.user # Link to the current logged-in user

            # Construct the prompt for the AI to strictly adhere to the desired format
            prompt_parts = [
                "Generate a highly professional, concise, and scannable plain-text resume from the following information. "
                "Adhere strictly to the requested format, mimicking the provided example's layout for headings and spacing.\n"
                "**Desired Output Example Format:**\n"
                "FULL NAME\n" # No bold for Full Name
                "Phone | Email | LinkedIn | GitHub\n\n"
                "SUMMARY\n\n" # Not bold
                "Your concise professional summary.\n\n"
                "EDUCATION\n\n" # Not bold
                "Degree | University | Expected Graduation: Year\n" # Not bold
                "* Bullet point for academic achievement/details\n\n"
                "EXPERIENCE\n\n" # Not bold
                "Job Title | Company Name | Start Date - End Date/Present\n" # Not bold
                "* Bullet point detailing responsibilities and achievements\n"
                "* Another bullet point\n\n"
                "SKILLS\n\n" # Not bold
                "Category 1: Skill1, Skill2, Skill3\n" # Category not bolded
                "Category 2: Skill4, Skill5\n\n"
                "PROJECTS\n\n" # Not bold
                "Project Name (Project URL if available)\n" # Not bold
                "* Bullet point describing project and your role\n"
                "* Another bullet point\n\n"
                "**Formatting Rules:**\n"
                "1.  **Full Name:** Displayed prominently at the very top, in ALL CAPS and *not bolded*.\n" # Corrected: Not bolded
                "2.  **Contact Information:** Follows the full name, on a single line, separated by ' | ' (not bolded).\n"
                "3.  **Section Headings (SUMMARY, EDUCATION, EXPERIENCE, SKILLS, PROJECTS):** All must be in ALL CAPS and *not bolded*, followed by two blank lines.\n" # Corrected: Not bolded
                "4.  **Bullet Points:** Use clear, concise bullet points for responsibilities, achievements, and descriptions. Each bullet point should start with an asterisk '*'.\n"
                "5.  **Education Details:** The main degree line (Degree | University | Expected Graduation) should *not* be bolded. Any additional details should be bulleted.\n"
                "6.  **Experience Details:** The job title, company name, and dates line should *not* be bolded. Descriptions under this should use bullet points.\n"
                "7.  **Projects Details:** The project name line should *not* be bolded. Descriptions under this should use bullet points.\n"
                "8.  **Skills Categorization:** Categorize skills explicitly (e.g., Languages: C, C++, Python), with the category name *not* bolded.\n" # Corrected: Category name not bolded
                "9.  **Omission:** If a section has *no* data, OMIT THAT SECTION ENTIRELY. Do not use 'N/A', 'Details not provided', or similar placeholders.\n"
                "10. **Output:** The response must be ONLY the resume content, suitable for direct copying, with no introductory or concluding remarks or conversational text.\n\n"
            ]

            # Full Name (Not bolded, ALL CAPS)
            prompt_parts.append(f"{resume_data.full_name.upper()}\n") # Removed ** for bolding

            # Contact Information
            contact_details = []
            if resume_data.phone:
                contact_details.append(resume_data.phone)
            if resume_data.email:
                contact_details.append(resume_data.email)
            if resume_data.linkedin_url:
                contact_details.append(resume_data.linkedin_url)
            if resume_data.github_url:
                contact_details.append(resume_data.github_url)
            if resume_data.portfolio_url:
                contact_details.append(resume_data.portfolio_url)
            
            if contact_details:
                prompt_parts.append(" | ".join(contact_details) + "\n\n")

            # Summary - Section heading NOT bolded
            if resume_data.summary:
                prompt_parts.append("SUMMARY\n\n" + resume_data.summary.strip() + "\n\n")

            # Education - Section heading NOT bolded
            if resume_data.education_level or resume_data.university_name or resume_data.degree or resume_data.graduation_year or resume_data.education_details:
                prompt_parts.append("EDUCATION\n\n")
                
                edu_main_line_parts = []
                if resume_data.degree:
                    edu_main_line_parts.append(resume_data.degree)
                if resume_data.university_name:
                    edu_main_line_parts.append(resume_data.university_name)
                
                if edu_main_line_parts:
                    # Main education line NOT bolded
                    prompt_parts.append(f"{' | '.join(edu_main_line_parts)}")
                    if resume_data.graduation_year:
                        prompt_parts.append(f" | Expected Graduation: {resume_data.graduation_year}\n") 
                    else:
                        prompt_parts.append("\n")
                
                if resume_data.education_details:
                    details = resume_data.education_details.strip().split('\n')
                    for detail in details:
                        if detail.strip():
                            prompt_parts.append(f"* {detail.strip()}\n")
                prompt_parts.append("\n") # Add a blank line for separation

            # Experience - Section heading NOT bolded
            has_experience_data = False
            experience_section_content = []

            if resume_data.job_title and resume_data.company_name:
                has_experience_data = True
                experience_period = ""
                if resume_data.start_date:
                    experience_period += f"{resume_data.start_date.strftime('%b %Y')} - "
                if resume_data.end_date: 
                    experience_period += f"{resume_data.end_date.strftime('%b %Y')}"
                else:
                    experience_period += "Present"

                # Job Title line NOT bolded
                experience_section_content.append(f"{resume_data.job_title} | {resume_data.company_name} | {experience_period}\n")
                
                if resume_data.experience_details:
                    details = resume_data.experience_details.strip().split('\n')
                    for detail in details:
                        if detail.strip():
                            experience_section_content.append(f"* {detail.strip()}\n")
            
            if resume_data.previous_experience:
                has_experience_data = True
                experience_section_content.append(f"\n{resume_data.previous_experience.strip()}\n")

            if has_experience_data:
                prompt_parts.append("EXPERIENCE\n\n")
                prompt_parts.extend(experience_section_content)
                prompt_parts.append("\n") # Add a blank line for separation


            # Skills - Section heading NOT bolded
            if resume_data.skills:
                prompt_parts.append("SKILLS\n\n")
                skills_list = [s.strip() for s in resume_data.skills.split(',') if s.strip()]
                
                # Provide structured categories for the AI to fill
                prompt_parts.append(
                    "Categorize the following skills into relevant sections like Languages, Frontend, Backend, Tools, etc., "
                    "and list them comma-separated under each category. Example: Languages: Python, JavaScript, C.\n" # Category name NOT bolded
                    "Skills to categorize from: "
                    f"{', '.join(skills_list)}\n\n"
                )

            # Projects - Section heading NOT bolded
            if resume_data.project_name and resume_data.project_description:
                prompt_parts.append("PROJECTS\n\n") 
                
                # Project name line NOT bolded
                project_line = f"{resume_data.project_name}"
                if resume_data.project_url:
                    project_line += f" ({resume_data.project_url})"
                prompt_parts.append(project_line + "\n")
                
                project_details = resume_data.project_description.strip().split('\n')
                for detail in project_details:
                    if detail.strip():
                        prompt_parts.append(f"* {detail.strip()}\n")
                prompt_parts.append("\n") # Add a blank line for separation


            full_prompt = "".join(prompt_parts).strip()
            # print("FULL PROMPT:\n", full_prompt) # Uncomment for debugging the prompt sent to AI

            try:
                # Call the Gemini API
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
                
                payload = {
                    "contents": [
                        {
                            "role": "user",
                            "parts": [
                                {"text": full_prompt}
                            ]
                        }
                    ]
                }
                headers = {
                    'Content-Type': 'application/json'
                }

                # Using requests library for the API call in Django views
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
                result = response.json()

                if result.get('candidates') and len(result['candidates']) > 0 and \
                   result['candidates'][0].get('content') and \
                   result['candidates'][0]['content'].get('parts') and \
                   len(result['candidates'][0]['content']['parts']) > 0:
                    generated_resume_text = result['candidates'][0]['content']['parts'][0]['text']
                    resume_data.generated_resume = generated_resume_text
                    resume_data.save() # Save the generated resume to the database
                else:
                    generated_resume_text = "AI could not generate a resume. Please try again or refine your input."
                    print("Unexpected AI response structure:", result) # For debugging
            except requests.exceptions.RequestException as e:
                generated_resume_text = f"Error connecting to AI: {e}"
                print(f"API Request Error: {e}")
            except json.JSONDecodeError as e:
                generated_resume_text = f"Error parsing AI response: {e}"
                print(f"JSON Decode Error: {e}, Response content: {response.text}")

    context = {
        'form': form,
        'generated_resume_text': generated_resume_text,
    }
    return render(request, 'resume_builder.html', context)


#=======================================================================================================================================================


from django.shortcuts import render

# ... (any other view functions you already have, like 'home' view) ...

def live_chat_view(request):
    """
    Renders the dedicated live_chat.html page.
    """
    return render(request, 'live_chat.html')

#=======================================================================================================================================================



def career_result_view(request):
    data = request.session.get('user_dashboard_data')
    if not data:
        return redirect('career_form')

    context = {
        **data['user_input'],
        'recommendation': data['ai_recommendation'],
    }
    return render(request, 'career_result2.html', context)
