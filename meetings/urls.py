from django.urls import path
from . import views

urlpatterns = [
    path('', views.create_meeting, name='create_meeting'),
    path('result/<int:id>/', views.meeting_result, name='meeting_result'),
    path('history/', views.meeting_history, name='meeting_history'),
    path('delete/<int:id>/', views.delete_meeting, name='delete_meeting'),
]
