# livechat/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import LiveChatSession, CounselorProfile
from django.http import JsonResponse
from django.db import transaction

# Helper to check if a user is a counselor
def is_counselor(user):
    return hasattr(user, 'counselorprofile') and user.counselorprofile.is_available

@login_required
def user_chat_request(request):
    # Logic to find an available counselor or create a new session
    # This is a simplified example. A real system would have a queuing mechanism.
    if request.method == 'POST':
        with transaction.atomic():
            # Try to find an available counselor
            available_counselor_profile = CounselorProfile.objects.filter(is_available=True).first()

            if available_counselor_profile:
                session = LiveChatSession.objects.create(
                    user=request.user,
                    counselor=available_counselor_profile.user,
                    is_active=True
                )
                return redirect('livechat:chat_room', room_name=session.id)
            else:
                # No counselor available, create a waiting session
                session = LiveChatSession.objects.create(
                    user=request.user,
                    is_active=True # Will be marked active once counselor joins
                )
                # Redirect to a waiting room or show a message
                return render(request, 'livechat/waiting_room.html', {'session_id': session.id})
    return render(request, 'livechat/live_chat_request.html')

@login_required
def chat_room(request, room_name):
    session = get_object_or_404(LiveChatSession, id=room_name)
    # Ensure only participants or counselor of this session can access
    if request.user != session.user and request.user != session.counselor:
        return redirect('livechat:user_chat_request') # Or show an error

    # You can fetch initial messages here if you want
    return render(request, 'livechat/chat_room.html', {
        'room_name': room_name,
        'user': request.user.username,
        'session_id': session.id,
        'counselor_name': session.counselor.username if session.counselor else 'Waiting for Counselor'
    })

@login_required
@user_passes_test(is_counselor)
def counselor_dashboard(request):
    # Counselors can see pending requests or active sessions
    active_sessions = LiveChatSession.objects.filter(counselor=request.user, is_active=True)
    pending_sessions = LiveChatSession.objects.filter(counselor__isnull=True, is_active=True)
    return render(request, 'livechat/counselor_dashboard.html', {
        'active_sessions': active_sessions,
        'pending_sessions': pending_sessions
    })

@login_required
@user_passes_test(is_counselor)
def counselor_join_session(request, session_id):
    session = get_object_or_404(LiveChatSession, id=session_id, counselor__isnull=True)
    if request.method == 'POST':
        session.counselor = request.user
        session.is_active = True # Mark active when counselor joins
        session.save()
        return redirect('livechat:chat_room', room_name=session.id)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400) # Or render a confirmation page


# livechat/views.py (continued)
# ... (existing imports and live chat views) ...

from .forms import AvailabilitySlotForm, AppointmentBookingForm
from django.db.models import Q # For complex queries

@login_required
@user_passes_test(is_counselor)
def counselor_add_availability(request):
    if request.method == 'POST':
        form = AvailabilitySlotForm(request.POST)
        if form.is_valid():
            slot = form.save(commit=False)
            slot.counselor = request.user
            slot.save()
            messages.success(request, 'Availability slot added successfully!')
            return redirect('livechat:counselor_dashboard') # Or a list of slots
        else:
            messages.error(request, 'Error adding slot. Please check your input.')
    else:
        form = AvailabilitySlotForm()
    return render(request, 'livechat/add_availability.html', {'form': form})


@login_required
def book_appointment(request):
    form = AppointmentBookingForm()
    counselor_id = request.GET.get('counselor') # For filtering slots by counselor

    if counselor_id:
        form = AppointmentBookingForm(counselor_id=counselor_id)

    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST)
        if form.is_valid():
            selected_slot = form.cleaned_data['slot']

            with transaction.atomic():
                # Ensure slot is not double booked
                slot_to_book = AvailabilitySlot.objects.select_for_update().get(id=selected_slot.id, is_booked=False)
                slot_to_book.is_booked = True
                slot_to_book.save()

                Appointment.objects.create(
                    user=request.user,
                    counselor=slot_to_book.counselor,
                    slot=slot_to_book,
                    start_time=slot_to_book.start_time,
                    end_time=slot_to_book.end_time,
                    status='confirmed', # Or 'pending' if counselor needs to confirm
                    # meeting_link=generate_meeting_link() # Implement a function to generate a link
                )
                messages.success(request, 'Appointment booked successfully!')
                return redirect('livechat:my_appointments')
        else:
            messages.error(request, 'Error booking appointment. Slot might already be taken.')

    # Get all available slots for display (not just via form's queryset)
    all_available_slots = AvailabilitySlot.objects.filter(is_booked=False, start_time__gte=timezone.now()).order_by('counselor__username', 'start_time')

    return render(request, 'livechat/book_appointment.html', {
        'form': form,
        'all_available_slots': all_available_slots,
        'counselors': CounselorProfile.objects.all(), # Pass all counselors for filtering
    })

@login_required
def my_appointments(request):
    user_appointments = Appointment.objects.filter(user=request.user).order_by('-start_time')
    counselor_appointments = Appointment.objects.filter(counselor=request.user).order_by('-start_time')
    return render(request, 'livechat/my_appointments.html', {
        'user_appointments': user_appointments,
        'counselor_appointments': counselor_appointments,
    })