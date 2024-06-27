from django.shortcuts import render
from .models import Room, Topic, Message,User
# Create your views her
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from . import forms
from django.shortcuts import HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.conf import settings


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('base:home')

    if request.method == 'POST':
        email = request.POST.get('email')
        email = email.lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)

        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, 'username or passsword does not exist')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('base:home')


def registerUser(request):
    page = 'register'
    if request.method == 'POST':
        form = forms.MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            login(request, user)
            return redirect('base:home')
        else:
            messages.error(request, 'An error occurred during registration')

    form = forms.MyUserCreationForm

    context = {'page': page, 'form': form}
    return render(request, 'base/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        # Q(host__name__icontains=q)
    )
    # rooms = Room.objects.all()
    # q = request.GET.get('q')

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q)|Q(room__name__icontains=q)|Q(room__description__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(pk=pk)
    room_messages = room.message_set.all()

    participants = room.participants.all()
    if request.method == 'POST':
        new_message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body'),

        )
        room.participants.add(request.user)
        return redirect('base:room', pk=room.id)
    context = {'room': room, 'room_messages': room_messages, 'participants': participants}
    return render(request, 'base/room.html', context)


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request, 'base/profile.html',context)




@login_required(login_url='base:login')
def createRoom(request):
    form = forms.RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)


        Room.objects.create(
                host=request.user,
                topic=topic,
                name=request.POST.get('name'),
                description=request.POST.get('description'),
            )
        return redirect('base:home')


    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='base:login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    topics = Topic.objects.all()
    form = forms.RoomForm(instance=room)

    if request.user != room.host:
        return HttpResponse('Only group admins can update the room')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('base:home')

    context = {'form': form,'topics': topics,'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='base:login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Only group admins can update the room')
    if request.method == 'POST':
        room.delete()
        return redirect('base:home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='base:login')
def deleteMessage(request, pk):
    t_message = Message.objects.get(id=pk)

    if request.user != t_message.user:
        return HttpResponse('Only message owner can delete')
    if request.method == 'POST':
        t_message.delete()
        return redirect('base:home')
    return render(request, 'base/delete.html', {'obj': t_message})

@login_required(login_url='base:login')
def updateUser(request):
    user = request.user
    form = forms.UserForm(instance=user)
    if request.method == 'POST':
        form = forms.UserForm(request.POST,request.FILES,instance=user)
        if form.is_valid :
            form.save()
            return redirect('base:profile',pk=user.id)
    context = {'form': form}
    return render(request, 'base/update_user.html',context)


def topics(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)

    context = {'topics': topics}
    return render(request, 'base/topics.html',context)


def activity(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html',{'room_messages':room_messages})
