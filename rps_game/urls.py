from django.urls import path
from . import views

urlpatterns = [
  path('', views.create_room, name='create_room'),
  path('room/<str:room_name>/', views.room, name='room'),
  path('check_room_status/<str:room_name>/', views.check_room_status, name='check_room_status'),
  path('game/<str:room_name>/', views.game, name='game'),
  path('save_move/', views.save_move, name='save_move'), 
  path('get_result/<str:room_name>/', views.get_result, name='get_result'),

]