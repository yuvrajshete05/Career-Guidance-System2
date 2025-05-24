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
