from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from datetime import date

# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, username, name, password=None):
        if not email:
            raise ValueError("Please provide a valid email address")
        if not username:
            raise ValueError("Please provide a valid username")
        if not name:
            raise ValueError("Please provide a valid name")

        user = self.model(
            email=self.normalize_email(email), username=username, name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, name, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            name=name,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=100, unique=True)
    username = models.CharField(verbose_name="username", max_length=50, unique=True)
    name = models.CharField(verbose_name="name", max_length=100)
    breed = models.CharField(max_length=30, null=True, blank=True)
    animal = models.CharField(max_length=50, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    date_of_birth = models.DateField(
        help_text="Please use the following format: <em>YYYY-MM-DD</em>.",
        null=True,
        blank=True,
    )
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now=False, auto_now_add=True
    )
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "name"]
    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
