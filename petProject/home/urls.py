from django.urls import path
from django.contrib.auth import login
from home import views

app_name = "home"
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/view/", views.view, name="view"),
    path("<int:pk>/edit/", views.edit_post, name="edit"),
    path("contact-us/", views.contact_us, name="contact"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("<str:username>/profile/", views.profile, name="profile"),
]
