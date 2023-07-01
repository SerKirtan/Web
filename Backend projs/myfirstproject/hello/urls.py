from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("kirtan", views.kirtan, name="kirtan"),
    path("<str:name>", views.greet, name="greet"),
]