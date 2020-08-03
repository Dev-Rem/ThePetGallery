from django.forms import ModelForm
from .models import Post, Comment, Image


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ("account", "is_active", "is_deleted", "is_archived", "id", "likes")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ("post", "account", "is_active", "is_deleted", "likes")


class ImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ("date", "account", "post")
