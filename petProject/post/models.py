from django.db import models

from user.models import Account

# Create your models here.


class Post(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True, null=False)
    caption = models.CharField(max_length=1000, null=True)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
    likes = models.IntegerField(default=0)
    image = models.ImageField(upload_to="images/", default="default_pet_img.jpg")


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500, null=True)
    likes = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=False, auto_now_add=True)
