from django.forms import ModelForm
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ("account", "id", "likes")


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = ("post", "likes")
