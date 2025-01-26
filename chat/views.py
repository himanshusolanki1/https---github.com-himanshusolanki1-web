from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Q
from .forms import SignUpForm
from .models import ChatRoom, Message
from django.contrib.auth.models import User

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('chat:index')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def index(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/index.html', {'users': users})

@login_required
def room(request, room_name):
    # Get or create chat room
    other_user = User.objects.get(username=room_name)
    room_name = f"{min(request.user.username, room_name)}_{max(request.user.username, room_name)}"
    
    chat_room, created = ChatRoom.objects.get_or_create(name=room_name)
    if created:
        chat_room.participants.add(request.user, other_user)
    
    # Get messages
    messages = Message.objects.filter(room=chat_room)
    
    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'other_user': other_user,
        'chat_messages': messages,
        'room_id': chat_room.id
    })
