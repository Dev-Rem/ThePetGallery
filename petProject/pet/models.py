from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date

# Create your models here.


class Pet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True, null=False)
    name = models.CharField(max_length=50, null=True)
    breed = models.CharField(max_length=30, null=True)
    animal = models.CharField(max_length=50, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to="images/", default="default_pet_img.jpg")
    date_of_birth = models.DateField(default=date.today())
    date = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.name
