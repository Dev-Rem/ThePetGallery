from django.urls import path
from django.contrib.auth import login
from . import views

app_name = "home"
urlpatterns = [
    path("", views.index, name="index"),
    path("contact-us/", views.contact_us, name="contact"),
]
