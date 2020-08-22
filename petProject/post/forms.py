from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from .models import Post, Comment, Image


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["caption"]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["comment"].label = ""


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["image"]
