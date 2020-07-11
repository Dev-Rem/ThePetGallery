from django.urls import path
from user import views

app_name = "user"
urlpatterns = [
    path("sign-up/", views.sign_up, name="sign_up"),
    path("profile/", views.profile, name="profile"),
]
