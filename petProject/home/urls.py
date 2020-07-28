from django.urls import path
from django.contrib.auth import login
from home import views

app_name = "home"
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_post, name="create"),
    path("<int:pk>/view/", views.view_post, name="view"),
    path("<int:pk>/edit/", views.edit_post, name="edit"),
    path("contact-us/", views.contact_us, name="contact"),
    path("sign-up/", views.sign_up, name="sign_up"),
    path("<int:pk>/profile/", views.profile, name="profile"),
    path("<int:pk>/edit-profile/", views.edit_profile, name="edit_profile"),
    path("<int:pk>/edit-comment", views.edit_comment, name="edit_comment"),
    path("<int:pk>/delete", views.delete_post, name="delete"),
]
