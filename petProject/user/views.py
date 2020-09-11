from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm, PasswordChangeForm
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from .models import Account, Follow
from .forms import SignUpForm, SignUpEditForm
from post.forms import ImageForm
from post.models import Post, Comment, Image

# Create your views here.
def password_reset_request(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data["email"]
            users = Account.objects.filter(Q(email=data) | Q(username=data))
            if users.exists():
                for user in users:
                    subject = "Password Reset Requested"
                    email_template_name = "password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        "domain": "127.0.0.1:8000",
                        "site_name": "The Pet Gallery",
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        "token": default_token_generator.make_token(user),
                        "protocol": "http",
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(
                            subject,
                            email,
                            "admin@example.com",
                            [user.email],
                            fail_silently=False,
                        )
                    except BadHeaderError:
                        return HttpResponse("Invalid header found.")
                    return redirect("/password_reset/done/")
    form = PasswordResetForm()
    return render(request, "password/password_reset.html", {"form": form},)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password was successfully updated")
            return redirect("home:profile")
        else:
            messages.error(request, "Oops something is not right")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "password/password_change.html", {"form": form})


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
        return redirect("/login")
    else:
        form = SignUpForm()
    return render(request, "registration/sign_up.html", {"form": form})


def profile_photo(request):
    account = Account.objects.get(email=request.user)
    if Image.objects.filter(account=account).exists():
        return redirect("home:index")
    else:
        if request.method == "POST":
            form = ImageForm(request.POST or None, request.FILES or None)
            if form.is_valid():
                photo = form.save(commit=False)
                photo.account = request.user
                if photo.image:
                    photo.save()
                else:
                    photo.image = "static/default_img.jpg"
                    photo.save()
                return redirect("home:index")
        else:
            form = ImageForm()
        return render(request, "profile/profile_photo.html", {"form": form})


def profile(request, username):
    account = Account.objects.get(username=username)
    posts = Post.objects.filter(account=account, is_active=True).order_by("-date")
    try:
        image = Image.objects.get(account=account)
        user_follow = Follow.objects.get(account=account)
        account_follow = Follow.objects.get(account=request.user)
        followers = user_follow.followers.all()
        following = user_follow.following.all()
        if request.method == "POST":
            if "follow" in request.POST:
                print(request.POST)
                follow2.followers.add(request.user)
                follow.following.add(account)
                follow2.save()
                follow.save()
                return redirect(request.path_info)
            if "unfollow" in request.POST:
                follow2.followers.remove(request.user)
                follow.following.remove(account)
                follow2.save()
                follow.save()
                return redirect(request.path_info)
    except:
        image = None
        follow2 = None
        follow = None

    return render(
        request,
        "profile/profile.html",
        {"account": account, "posts": posts, "image": image},
    )


def edit_profile(request, username):
    form_class = SignUpEditForm
    account = get_object_or_404(Account, username=username)
    form = form_class(request.POST, request.FILES, instance=account)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(request, "Profile successfully updated")
            return redirect("profile:profile", username=request.user.username)
    else:
        form = SignUpEditForm(instance=account)
    return render(request, "profile/edit_profile.html", {"form": form})


def follow(request, username):
    try:
        follow = Follow.objects.get(account=request.user)
        followers = follow.followers.all()
        following = follow.following.all()
        if request.method == "POST":
            print(request.POST)
            if "follow" in request.POST:
                account = Account.objects.get(email=request.POST.get("follow"))
                print(request.POST.get("follow"))
                following.add(request.user)
                following.save()
                return redirect(request.path_info)
            if "unfollow" in request.POST:
                print(request.POST.get("unfollow"))
                account = Account.objects.get(email=request.POST.get("unfollow"))
                following.remove()
                following.save()
                return redirect(request.path_info)
    except DoesNotExist:
        follow = None

    return render(
        request,
        "profile/follow.html",
        {"follow": follow, "followers": followers, "following": following},
    )
    pass
