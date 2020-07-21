from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from post.forms import PostForm, CommentForm
from user.forms import SignUpForm
from user.models import Account
from post.models import Post, Comment
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required
def index(request):
    posts = Post.objects.order_by("-date")
    return render(request, "home/index.html", {"posts": posts,})


def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.account = request.user
            new_post.save()
            return redirect("home:index")
    else:
        form = PostForm()
    return render(request, "home/create.html", {"form": form})


def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    form = PostForm(request.POST, request.FILES, instance=post)
    if request.method == "POST":
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("home:index")
    else:
        form = PostForm(instance=post)
    return render(request, "home/edit.html", {"form": form})


def view_post(request, pk):
    form_class = CommentForm
    form = form_class(request.POST or None)
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by("-date")
    if request.method == "POST":
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(request.path_info)
    return render(
        request, "home/view.html", {"post": post, "comments": comments, "form": form}
    )


def edit_comment(request, pk):
    form_class = CommentForm
    comment = get_object_or_404(Comment, pk)
    form = form_class(request.POST, instance=comment)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("view_post",)
    return render(request, "home/edit_comment.html", {"form": form})


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect("/login")
    else:
        form = SignUpForm()
    return render(request, "home/sign_up.html", {"form": form})


def profile(request, username):
    account = Account.objects.get(username=username)
    return render(request, "home/profile.html", {"account": account})


def edit_profile(request):
    pass


def contact_us(request):
    return render(request, "home/contact_us.html", {})
