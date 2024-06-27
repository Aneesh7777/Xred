from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'base'
urlpatterns = [
    path('login/',views.loginPage,name='login'),
    path('logout/',views.logoutUser,name='logout'),
    path('register/',views.registerUser,name='register'),

    path('',views.home,name='home'),
    path('update-room/<int:pk>/',views.updateRoom,name='updateRoom'),
    path('room/<int:pk>/',views.room,name='room'),
    path('profile/<int:pk>/',views.userProfile,name='profile'),

    path('create-room/',views.createRoom,name='createRoom'),
    path('delete-room/<int:pk>/',views.deleteRoom,name='deleteRoom'),
    path('delete-message/<int:pk>/',views.deleteMessage,name='deleteMessage'),
    path('update-user/',views.updateUser,name='updateUser'),
    path('topics/',views.topics,name='topics'),
    path('activity/',views.activity,name='activity'),


]
