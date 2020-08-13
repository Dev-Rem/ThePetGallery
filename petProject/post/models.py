from django.db import models
from user.models import Account


# Create your models here.


class Post(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True, null=False)
    caption = models.CharField(max_length=1000, null=True)
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    likes = models.ManyToManyField(Account, related_name="like_post", blank=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)


class Comment(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    likes = models.ManyToManyField(Account, related_name="like_comment", blank=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)


class Image(models.Model):
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="images/", null=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
