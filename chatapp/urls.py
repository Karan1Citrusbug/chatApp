from django.urls import path
from . import views


urlpatterns = [
    path("",views.home,name="home"),
    path('chat/<str:user>/<str:room_name>/<str:token>/', views.room, name='room'),
    path('generate-token/<str:user>/<str:room_name>/', views.generate_token, name='token'),
    path('delete/<int:id>/<str:token>/',views.deletemessage,name='delete'),
]
