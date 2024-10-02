from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, RoomUser, Message
from .form import RoomForm
from django.contrib.auth.models import User  # Make sure to import User
from .forms import  RoomForm , MessageForm
@login_required
def rooms(request):
    # Get rooms for the current user
    rooms = Room.objects.filter(users=request.user)

    return render(request, 'room/rooms.html', {'rooms': rooms})


@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)
    
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.room = room
            message.save()
            return redirect('room', slug=slug)

    messages = Message.objects.filter(room=room)[0:25]
    form = MessageForm()  # Create an empty form

    return render(request, 'room/room.html', {'room': room, 'messages': messages, 'form': form})


@login_required
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST, current_user=request.user)  # Pass the current user
        if form.is_valid():
            room = form.save(commit=False)
            room.slug = room.name.replace(' ', '-').lower()  # Create a slug from the room name
            room.save()
            # Automatically add the creator to the room
            room.users.add(request.user)
            # Add selected users to the room
            users = form.cleaned_data['users']
            room.users.add(*users)  # Use * to unpack the list of users
            room.save()
            return redirect('rooms')  # Redirect to the rooms list after creating
    else:
        form = RoomForm(current_user=request.user)  # Pass the current user
    
    return render(request, 'room/create_room.html', {'form': form})

