from django.urls import path
from . import views

urlpatterns = [
    path("", views.BookAPIView.as_view()),
    path("<int:pk>/", views.BookAPIView.as_view()),
]