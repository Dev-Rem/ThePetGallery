from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from post.forms import PostForm, CommentForm, ImageForm
from user.forms import SignUpForm, SignUpEditForm
from post.models import Post, Comment, Image
from user.models import Account


# Create your views here.


@login_required
def index(request):
    posts = Post.objects.filter(is_active=True).order_by("-date",)
    images = None
    comments = None
    for post in posts:
        images = post.image_set.all()
        comments = Comment.objects.filter(post=post, is_active=True).order_by("-date")
    return render(
        request,
        "home/index.html",
        {"posts": posts, "images": images, "comments": comments},
    )


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
        return render(request, "home/profile_photo.html", {"form": form})


def profile(request, username):
    account = Account.objects.get(username=username)
    try:
        image = Image.objects.get(account=account)
    except:
        image = None
    posts = Post.objects.filter(account=account, is_active=True).order_by("-date")
    return render(
        request,
        "home/profile.html",
        {"account": account, "posts": posts, "image": image},
    )


def edit_profile(request, username):
    form_class = SignUpEditForm
    account = get_object_or_404(Account, username=username)
    form = form_class(request.POST, request.FILES, instance=account)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("home:profile", username=username)
    else:
        form = SignUpEditForm(instance=account)
    return render(request, "home/edit_profile.html", {"form": form})


def contact_us(request):
    return render(request, "home/contact_us.html", {})
