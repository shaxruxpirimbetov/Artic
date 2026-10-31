from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListCreateUser.as_view()),
    path("<int:pk>/", views.DetailUser.as_view()),
    path("me/", views.MeAPIView.as_view()),
]