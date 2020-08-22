from django.urls import path
from django.contrib.auth import login
from . import views

app_name = "post"

urlpatterns = [
    path("create/", views.create_post, name="create"),
    path("<int:pk>/view/", views.view_post, name="view"),
    path("<int:pk>/edit/", views.edit_post, name="edit"),
    path("<int:pk>/edit-comment", views.edit_comment, name="edit_comment"),
    path("<int:pk>/delete", views.delete_post, name="delete"),
    path("<str:username>/archive/", views.archive_post, name="archive_post"),
]
