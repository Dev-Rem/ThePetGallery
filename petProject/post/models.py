from django.db import models
from user.models import Account


# Create your models here.


class Post(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True, null=False)
    caption = models.CharField(max_length=1000, null=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    likes = models.ManyToManyField(Account, related_name="likes", blank=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, null=True)
    likes = models.ManyToManyField(Account, related_name="comment_likes", blank=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)


class Image(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/",)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
