from django.urls import path
from django.contrib.auth import login
from . import views

app_name = "home"
urlpatterns = [
    path("", views.index, name="index"),
    path("contact-us/", views.contact_us, name="contact"),
    path("<str:username>/profile/", views.profile, name="profile"),
    path("<str:username>/edit-profile/", views.edit_profile, name="edit_profile"),
    path("profile-photo/", views.profile_photo, name="profile_photo"),
]
