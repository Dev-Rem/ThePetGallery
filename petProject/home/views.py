from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from post.forms import PostForm, CommentForm, ImageForm
from user.forms import SignUpForm
from user.models import Account
from post.models import Post, Comment, Image
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.urls import reverse


# Create your views here.


@login_required
def index(request):
    posts = Post.objects.order_by("-date")
    return render(request, "home/index.html", {"posts": posts,})


def create_post(request):
    ImageFormSet = formset_factory(ImageForm, extra=2, max_num=2)
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        image_form = ImageForm(request.POST or None, request.FILES or None)
        if form.is_valid() and image_form.is_valid():
            new_post = form.save(commit=False)
            new_post.account = request.user
            new_post.save()

            image = image_form.save(commit=False)
            image.post = new_post
            image.save()

            return redirect("home:index")
    else:
        form = PostForm()
        image_form = ImageForm()
    return render(request, "home/create.html", {"form": form, "image_form": image_form})


def edit_post(request, pk):
    image_form_class = ImageForm
    post = get_object_or_404(Post, pk=pk)
    image = Image.objects.get(post=post)
    form = PostForm(request.POST, instance=post)
    image_form = image_form_class(request.POST, files=request.FILES, instance=image)
    if request.method == "POST":
        if form.is_valid() and image_form.is_valid():
            form.save()
            photo = Image(post=post, image=image_form.cleaned_data.get("image"))
            d = Image.objects.get(id=image.id)
            d.image = photo.image
            d.save()
            return redirect("/" + str(post.id) + "/view/")
    else:
        form = PostForm(instance=post)
    return render(
        request, "home/edit_post.html", {"form": form, "image_form": image_form}
    )


def view_post(request, pk):
    form_class = CommentForm
    form = form_class(request.POST or None)
    post = get_object_or_404(Post, pk=pk)
    image = get_object_or_404(Image, post=post)
    comments = Comment.objects.filter(post=post).order_by("-date")
    if request.method == "POST":
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return HttpResponseRedirect(request.path_info)

    return render(
        request,
        "home/view.html",
        {"post": post, "comments": comments, "form": form, "image": image,},
    )


def edit_comment(request, pk):
    form_class = CommentForm
    comment = get_object_or_404(Comment, pk=pk)
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


def edit_profile(request, username):
    account = get_object_or_404(Account, username=username)
    form = form_class(request.POST, request.FILES, instance=account)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("home:profile")
    else:
        form = PostForm(instance=post)
    return render(request, "home/edit.html", {"form": form})
    pass


def contact_us(request):
    return render(request, "home/contact_us.html", {})
