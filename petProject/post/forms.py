from django.forms import ModelForm
from .models import Post, Comment, Image


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["caption"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["image"]
