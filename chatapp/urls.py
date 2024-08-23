from django.urls import path
from . import views

urlpatterns = [
    path("",views.home),
    path('chat/<str:user>/<str:room_name>/', views.room, name='room'),
]
