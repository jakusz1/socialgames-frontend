from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('games/', views.GameSessionView.as_view()),
    path('games/<uri>/', views.GameSessionView.as_view()),
    path('games/<uri>/start', views.GameStartView.as_view()),
    path('games/<uri>/tasks/', views.GameSessionTaskView.as_view()),
    path('tasks/<task_id>/answers/', views.GameSessionAnswerView.as_view()),
    path('tasks/<task_id>/choices/', views.GameSessionChoiceView.as_view()),
]
