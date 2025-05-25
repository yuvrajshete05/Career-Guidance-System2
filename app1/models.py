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
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"