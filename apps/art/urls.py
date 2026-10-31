from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListCreateArt.as_view()),
    path("<int:id>/", views.DetailArt.as_view()),
]