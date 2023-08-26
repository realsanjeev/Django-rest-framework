from django.urls import path
from . import views

urlpatterns = [
    path("create/", views.BookCreateAPIView.as_view()),
    path("<int:pk>/", views.BookDetailAPIView.as_view()),
    path("<int:pk>/update/", views.BookUpdateAPIView.as_view()),
    path("<int:pk>/delete/", views.BookDestroyerAPIView.as_view())
]