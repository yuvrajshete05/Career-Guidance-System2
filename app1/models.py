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