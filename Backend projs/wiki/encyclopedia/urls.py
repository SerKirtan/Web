from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:TITLE>" , views.entry, name="wiki_entry"),
    path("search" , views.search, name="search"),
    path("random" , views.random, name="random"),
    path("newpage", views.newpage, name="newpage"),
    path("edit/<str:title>", views.edit, name="edit"), 
]
