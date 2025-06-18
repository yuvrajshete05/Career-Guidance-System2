from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class CareerForm(forms.Form):
    full_name = forms.CharField(label="Full Name", max_length=100)
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    age = forms.IntegerField()
    ug_course = forms.ChoiceField(choices=[('BTech', 'B.Tech'), ('BSc', 'B.Sc'), ('BA', 'B.A')])
    ug_specialization = forms.CharField(label="UG Specialization")
    cgpa = forms.FloatField(min_value=0.0, max_value=10.0)
    interests = forms.CharField(help_text="Comma-separated, e.g., AI, Web")
    skills = forms.CharField(help_text="Comma-separated, e.g., Python, SQL")
    certifications = forms.CharField(help_text="Comma-separated, e.g., Coursera ML")
    working = forms.ChoiceField(choices=[('Yes', 'Yes'), ('No', 'No')])
    current_job = forms.CharField(label="Current Job Title (or NA)", required=False)
    masters = forms.CharField(label="Master's Degree Field (or NA)", required=False)
