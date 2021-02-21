from django.db import models
from django.contrib.auth.models import AbstractBaseUser, \
                                       PermissionsMixin, \
                                       BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, name, email, password):
        if not email:
            raise ValueError("Email field is required")

        email = self.normalize_email(email)
        user = self.model(name=name, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_super_user(self, name, email, password):
        user = self.create_user(name, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('name',)

    def __str__(self):
        return self.name
