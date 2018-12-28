from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('games/', views.GameView.as_view()),
    path('games/<uri>/', views.GameView.as_view()),
    path('games/<uri>/start', views.GameStartView.as_view()),
    path('games/<uri>/rounds/', views.AllRoundsView.as_view()),
    path('games/<uri>/round', views.FirstRoundView.as_view()),
    path('rounds/<round_id>/answers/', views.AnswerView.as_view()),
]
