# chatbot/admin.py

# Import models from the chatbot app itself
from .models import Conversation # Assuming Conversation is in chatbot/models.py

# If you want to register LiveChat models in the admin,
# you MUST import them from the livechat app's models.
# It's generally better to register an app's models in its own admin.py.
# So, you might want to move these imports to livechat/admin.py instead.
# If you insist on registering them here for some reason, the import would be:
# from livechat.models import LiveChatSession, LiveChatMessage, CounselorProfile, AvailabilitySlot, Appointment

from django.contrib import admin

# Register your models here.
admin.site.register(Conversation)

# If you keep the LiveChat model registrations in chatbot/admin.py,
# you would uncomment the import above and register them here too.
# However, best practice is to put livechat model registrations in livechat/admin.py
# admin.site.register(LiveChatSession)
# admin.site.register(LiveChatMessage)
# admin.site.register(CounselorProfile)
# admin.site.register(AvailabilitySlot)
# admin.site.register(Appointment)