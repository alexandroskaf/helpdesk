from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from .models import Room, RoomUser, Message
from .form import RoomForm
from django.contrib.auth.models import User  # Make sure to import User
@login_required
def rooms(request):
    rooms = Room.objects.all()
    return render(request, 'room/rooms.html', {'rooms': rooms})

@login_required
def room(request, slug):
    room = get_object_or_404(Room, slug=slug)

    # Restrict access to users who are in the RoomUser model
    if not RoomUser.objects.filter(room=room, user=request.user).exists():
        return redirect('rooms')  # Redirect to rooms list if the user is not allowed

    messages = Message.objects.filter(room=room)[0:25]
    return render(request, 'room/room.html', {'room': room, 'messages': messages})

@user_passes_test(lambda u: u.is_superuser)
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            selected_users = request.POST.getlist('selected_users')  # Get the list of user IDs from the form
            for user_id in selected_users:
                user = User.objects.get(id=user_id)
                RoomUser.objects.create(room=room, user=user)  # Create the RoomUser instance
            return redirect('rooms')  # Redirect to the room list
    else:
        form = RoomForm()

    return render(request, 'room/create_room.html', {'form': form})


