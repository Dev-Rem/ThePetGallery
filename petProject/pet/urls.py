from django.urls import path
from pet import views


app_name = "pet"
urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/view/", views.view, name="view"),
    path("<int:pk>/edit/", views.edit, name="edit"),
    path("contact-us/", views.contact_us, name="contact"),
]
