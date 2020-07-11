from django.shortcuts import render, redirect, get_object_or_404
from .forms import SignUpForm
from django.contrib.auth.models import User


# Create your views here.
def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if sign_up_form.is_valid():
            sign_up_form.save()
        return redirect("pet:index")
    else:
        form = SignUpForm()

    return render(request, "user/sign_up.html", {"form": form})


def profile(request):
    user = get_object_or_404(User, username=request.user)
    return render(request, "user/profile.html", {"user": user})
