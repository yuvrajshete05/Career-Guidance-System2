# livechat/models.py
from django.db import models
from django.contrib.auth.models import User

class LiveChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='user_chat_sessions')
    counselor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='counselor_chat_sessions')
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    # You might add a 'status' field: 'waiting', 'in_progress', 'ended'

    def __str__(self):
        return f"Session {self.id} - User: {self.user.username if self.user else 'N/A'}"

class LiveChatMessage(models.Model):
    session = models.ForeignKey(LiveChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE) # The user who sent the message
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"

# Optional: Counselor Profile (if not already in user_profiles)
class CounselorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=False) # For live chat status
    specialization = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username + " (Counselor)"
    

# livechat/models.py (continued)

# ... (existing models) ...

class AvailabilitySlot(models.Model):
    counselor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability_slots')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    class Meta:
        unique_together = ('counselor', 'start_time') # Prevent exact overlapping slots
        ordering = ['start_time']

    def __str__(self):
        return f"{self.counselor.username}'s slot: {self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.end_time.strftime('%H:%M')}"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_appointments')
    counselor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='counselor_appointments')
    slot = models.OneToOneField(AvailabilitySlot, on_delete=models.SET_NULL, null=True, blank=True) # Link to a slot
    start_time = models.DateTimeField() # Duplicate for convenience, but slot is source of truth
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('cancelled', 'Cancelled'), ('completed', 'Completed')], default='pending')
    meeting_link = models.URLField(blank=True, null=True) # E.g., Zoom/Google Meet link
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"Appt for {self.user.username} with {self.counselor.username} at {self.start_time.strftime('%Y-%m-%d %H:%M')}"    