# chatbot/models.py
from django.db import models
from django.contrib.auth.models import User # Assuming you use Django's default User model

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('assistant', 'Assistant')])
    message = models.TextField()

    class Meta:
        ordering = ['timestamp'] # Order conversations chronologically

    def __str__(self):
        return f"{self.user.username} - {self.role}: {self.message[:50]}"