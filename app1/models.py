from django.db import models

class Career(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

class Skill(models.Model):
    name = models.CharField(max_length=100)
    detail = models.TextField()

class Course(models.Model):
    name = models.CharField(max_length=100)
    overview = models.TextField()
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)  # Add this field


# loginform/models.py
from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# app1/models.py

from django.db import models

class Login(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=128)  # Usually hashed, but for example plain text here

    def __str__(self):
        return self.username
