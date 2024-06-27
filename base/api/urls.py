from django.urls import path
from . import views

urlpatterns = [
    path('',views.getRoutes),
    path('rooms/',views.getRooms),
    path('rooms/<int:pk>/',views.getRoom),
    path('topics/',views.getTopics),
    path('topics/<int:pk>',views.getTopic),
]
