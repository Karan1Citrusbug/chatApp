from django.urls import path
from . import views


urlpatterns = [
    path("",views.home,name="home"),
    path('chat/<str:user>/<str:room_name>/', views.room, name='room'),
    path('delete/<int:id>/',views.deletemessage,name='delete'),
]
