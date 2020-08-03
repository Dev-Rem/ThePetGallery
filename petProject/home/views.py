from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from post.models import Post, Comment, Image
from post.forms import PostForm, CommentForm, ImageForm
from user.forms import SignUpForm, SignUpEditForm
from user.models import Account


# Create your views here.


@login_required
def index(request):
    posts = Post.objects.filter(is_active=True).order_by("-date",)
    for post in posts:
        if request.method == "POST":
            if "like" in request.POST:
                post.likes.add(request.user)
                post.save()
                return redirect(request.path_info)
            elif "dislike" in request.POST:
                post.likes.remove(request.user)
                post.save()
                return redirect(request.path_info)
    return render(request, "home/index.html", {"posts": posts})


def create_post(request):
    ImageFormSet = formset_factory(ImageForm, extra=3, max_num=3)
    if request.method == "POST":
        form = PostForm(request.POST or None)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        for image_dict in formset.cleaned_data:
            if "image" in image_dict.keys():
                if form.is_valid() and formset.is_valid():
                    post = form.save(commit=False)
                    post.account = request.user
                    post.save()
                    print(formset.cleaned_data)
                    for image_form in formset.cleaned_data:
                        if not image_form:
                            continue
                        else:
                            image = Image(post=post, image=image_form["image"])
                            image.save()
                    return redirect("home:index")
                break
            else:
                return redirect(request.path_info)
    else:
        form = PostForm()
        formset = ImageFormSet()
    return render(request, "home/create.html", {"form": form, "formset": formset})


def edit_post(request, pk):
    image_form_class = ImageForm
    post = get_object_or_404(Post, pk=pk)
    ImageFormSet = formset_factory(ImageForm, extra=3, max_num=3)
    form = None
    formset = None
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
        if form.is_valid() and formset.is_valid():
            form.save()
            data = Image.objects.filter(post=post)
            for index, form in enumerate(formset):
                if form.cleaned_data:
                    if form.cleaned_data["id"] is None:
                        photo = Image(post=post, image=form.cleaned_data.get("image"))
                        photo.save()
                    else:
                        photo = Image(post=post, image=form.cleaned_data.get("image"))
                        d = Image.objects.get(id=data[index].id)
                        d.image = photo.image
                        d.save()
            return redirect("home:view", pk=post.id)
    else:
        form = PostForm(instance=post)
        # queryset giving issues fix ASAP
        formset = ImageFormSet(queryset=Image.objects.filter(post=post))
    return render(request, "home/edit_post.html", {"form": form, "formset": formset})


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    images = Image.objects.filter(post=post)
    if request.method == "POST":
        post.is_active = False
        post.is_deleted = True
        post.save()
        return redirect("home:index")
    return render(request, "home/delete_post.html", {"post": post, "images": images})


def archive(request, username):
    account = Account.objects.get(username=username)
    posts = Post.objects.filter(is_archived=True, account=account).order_by("-date",)
    images = None
    for post in posts:
        images = post.image_set.all()
    if request.method == "POST":
        post.is_active = True
        post.is_archived = False
        post.save()
        return redirect("home:index")
    return render(request, "home/archive.html", {"posts": posts, "images": images})


def view_post(request, pk):
    form_class = CommentForm
    form = form_class(request.POST or None)
    post = get_object_or_404(Post, pk=pk, is_active=True)
    images = Image.objects.filter(post=post)
    comments = Comment.objects.filter(post=post, is_active=True).order_by("-date")
    if request.method == "POST":
        if "comment" in request.POST:
            if form.is_valid():
                new_comment = form.save(commit=False)
                new_comment.post, new_comment.account = post, request.user
                new_comment.save()
                return redirect(request.path_info)
        elif "archive" in request.POST:
            post.is_active, post.is_archived = False, True
            post.save()
            return redirect("home:index")
        elif "like" in request.POST:
            post.likes.add(request.user)
            post.save()
            return redirect(request.path_info)
        elif "dislike" in request.POST:
            post.likes.remove(request.user)
            post.save()
            return redirect(request.path_info)
        elif "like_comment" in request.POST:
            comment = Comment.objects.get(pk=request.POST.get("like_comment"))
            comment.likes.add(request.user)
            comment.save()
        elif "dislike_comment" in request.POST:
            comment = Comment.objects.get(pk=request.POST.get("dislike_comment"))
            comment.likes.remove(request.user)
            comment.save()
        elif "delete_comment" in request.POST:
            comment = Comment.objects.get(pk=request.POST.get("delete_comment"))
            comment.is_active, comment.is_deleted = False, True
            comment.save()
    return render(
        request,
        "home/view.html",
        {"post": post, "comments": comments, "form": form, "images": images,},
    )


def edit_comment(request, pk):
    form_class = CommentForm
    comment = get_object_or_404(Comment, pk=pk)
    edit_comment_form = form_class(request.POST or None, instance=comment)
    if request.method == "POST":
        if edit_comment_form.is_valid():
            comment.comment = edit_comment_form.cleaned_data["comment"]
            comment.save()
            return redirect("home:view", pk=comment.post.id)
    return render(
        request, "home/edit_comment.html", {"edit_comment_form": edit_comment_form}
    )


def sign_up(request):
    if request.method == "POST":
        form = SignUpForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            form.save()
        return redirect("/login")
    else:
        form = SignUpForm()
    return render(request, "home/sign_up.html", {"form": form})


def profile_photo(request):
    try:
        account = Account.objects.get(email=request.user)
        if Image.objects.filter(account=account).exists():
            return redirect("home:index")
    except:
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
        print(form.data)
        if form.is_valid():
            # account.profile_photo = form.cleaned_data["profile_photo"]
            account.name = form.cleaned_data["name"]
            account.username = form.cleaned_data["username"]
            account.email = form.cleaned_data["email"]
            account.breed = form.cleaned_data["breed"]
            account.animal = form.cleaned_data["animal"]
            account.bio = form.cleaned_data["bio"]
            account.date_of_birth = form.cleaned_data["date_of_birth"]
            account.save()
            return redirect("home:profile", username=username)
    else:
        form = SignUpEditForm(instance=account)
    return render(request, "home/edit_profile.html", {"form": form})


def contact_us(request):
    return render(request, "home/contact_us.html", {})
