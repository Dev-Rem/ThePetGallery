from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from post.forms import PostForm, CommentForm
from user.forms import SignUpForm
from user.models import Account
from post.models import Post, Comment
from django.http import HttpResponseRedirect


# Create your views here.

# class IndexView()
def index(request):
    posts = Post.objects.order_by("-date")
    return render(request, "home/index.html", {"posts": posts,})


def create(request):
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


def view(request, pk):
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


def edit_post(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    form = PetForm(instance=pet)
    if request.method == "POST":
        form = PetForm(instance=pet, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("home:index")
    else:
        form = PetForm(instance=pet)
    return render(request, "home/edit.html", {"form": form})


def edit_comment(request):
    pass


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


def contact_us(request):
    return render(request, "home/contact_us.html", {})
