from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
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
        comments = Comment.objects.filter(post=post, is_active=True, reply=None)
    return render(
        request,
        "home/index.html",
        {"posts": posts, "images": images, "comments": comments},
    )


def contact_us(request):
    return render(request, "home/contact_us.html", {})
