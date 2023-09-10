from django.urls import path
from . import views

urlpatterns = [
    path("", views.SearchListView.as_view()),
    path("v2/", views.SearchAlgoliaListView.as_view()),
]
