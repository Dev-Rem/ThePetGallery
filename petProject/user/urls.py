from django.urls import path
from . import views
from django.contrib.auth import login
from django.contrib.auth import views as auth_views

app_name = "main"


urlpatterns = [
    path("sign-up/", views.sign_up, name="sign_up"),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path("password_change/", views.change_password, name="change_password"),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password/password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
