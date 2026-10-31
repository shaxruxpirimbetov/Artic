from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListCreateComment.as_view()),
    path("<int:pk>/", views.DetailComment.as_view()),
]