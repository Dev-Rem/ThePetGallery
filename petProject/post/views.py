from django.shortcuts import render, redirect, get_object_or_404
from django.forms import formset_factory
from django.contrib import messages
from .models import Post, Comment, Image
from .forms import PostForm, CommentForm, ImageForm
from user.models import Account
from django.template.loader import render_to_string
from django.http import JsonResponse

# Create your views here.


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
                    messages.success(request, "Post successfully created")
                    return redirect("home:index")
                break
            else:
                messages.error(request, "No image added")
                return redirect(request.path_info)
    else:
        form = PostForm()
        formset = ImageFormSet()
    return render(request, "post/create.html", {"form": form, "formset": formset})


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
                    print(form.cleaned_data)
                    if form.cleaned_data["image"] is None:
                        photo = Image(post=post, image=form.cleaned_data.get("image"))
                        photo.save()
                    else:
                        photo = Image(post=post, image=form.cleaned_data.get("image"))
                        d = Image.objects.get(id=data[index].id)
                        d.image = photo.image
                        d.save()
            return redirect("post:view", pk=post.id)
    else:
        form = PostForm(instance=post)
        formset = ImageFormSet(request.POST or None, request.FILES or None)
    return render(
        request, "post/edit_post.html", {"form": form, "formset": formset, "post": post}
    )


def view_post(request, pk):
    form_class = CommentForm
    form = form_class(request.POST or None)
    post = get_object_or_404(Post, pk=pk)
    images = Image.objects.filter(post=post)
    post_liked = False
    comment_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post_liked = True
    comments = Comment.objects.filter(post=post, is_active=True, reply=None).order_by(
        "-date"
    )
    if request.method == "POST":
        if "comment" in request.POST:
            if form.is_valid():
                reply_id = request.POST.get("comment_id")
                comment_qs = None
                if reply_id:
                    print(reply_id)
                    comment_qs = Comment.objects.get(id=reply_id)
                    print(comment_qs)
                new_comment = form.save(commit=False)
                new_comment.post, new_comment.account, new_comment.reply = (
                    post,
                    request.user,
                    comment_qs,
                )
                new_comment.save()
        return redirect(request.path_info)

        if "like_post" in request.POST:
            post.likes.add(request.user)
            post.save()
            post_liked = True
            return redirect(request.path_info)
        if "dislike_post" in request.POST:
            post.likes.remove(request.user)
            post.save()
            post_liked = False
            return redirect(request.path_info)
        if "like_comment" in request.POST:
            comment = Comment.objects.get(pk=request.POST.get("like_comment"))
            comment.likes.add(request.user)
            comment.save()
            comment_liked = True
            return redirect(request.path_info)
        if "dislike_comment" in request.POST:
            comment = Comment.objects.get(pk=request.POST.get("dislike_comment"))
            comment.likes.remove(request.user)
            comment.save()
            comment_liked = False
            return redirect(request.path_info)
    return render(
        request,
        "post/view.html",
        {
            "post": post,
            "comments": comments,
            "form": form,
            "images": images,
            "post_liked": post_liked,
            # "comment_liked": comment_liked,
        },
    )


def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    images = Image.objects.filter(post=post)
    comments = Comment.objects.filter(post=post, is_active=True).order_by("-date")
    if request.method == "POST":
        if "delete_post" in request.POST:
            post.is_active, post.is_deleted = False, True
            post.save()
            return redirect("home:index")
        if "delete_comment" in request.POST:
            comment = Comment.objects.get(pk=request.POST.get("delete_comment"))
            comment.is_active, comment.is_deleted = False, True
            comment.save()
            return redirect("post:view", pk=pk)
    return render(
        request,
        "post/delete_post.html",
        {"post": post, "images": images, "comments": comments},
    )


def edit_comment(request, pk):
    form_class = CommentForm
    comment = get_object_or_404(Comment, pk=pk)
    form = form_class(request.POST or None, instance=comment)
    print(comment.post.id)
    if request.method == "POST":
        if form.is_valid():
            comment.comment = form.cleaned_data["comment"]
            comment.save()
            return redirect("post:view", pk=comment.post.id)
    return render(request, "post/edit_comment.html", {"form": form, "comment": comment})


def archive_post(request, username):
    account = Account.objects.get(username=username)
    posts = Post.objects.filter(is_archived=True, account=account).order_by("-date",)
    images = None
    comments = None
    for post in posts:
        images = post.image_set.all()
        comments = Comment.objects.filter(post=post, is_active=True).order_by("-date")
    if request.method == "POST":
        if "archive_post" in request.POST:
            post = Post.objects.get(id=request.POST.get("post_id"))
            post.is_active, post.is_archived = False, True
            post.save()
            return redirect("home:index")
        if "unarchive_post" in request.POST:
            post = Post.objects.get(id=request.POST.get("post_id"))
            post.is_active, post.is_archived = True, False
            post.save()
            return redirect("home:index")
    return render(
        request,
        "post/archive.html",
        {"posts": posts, "images": images, "comments": comments},
    )
