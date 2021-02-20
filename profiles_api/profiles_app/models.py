from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


class UserProfileManager(BaseUserManager):
    """Manager for our user model

    Args:
        BaseUserManager (UserManager): Contributed by django users
    """
    def create_user(self, email, name, password):
        """Creates new user

        Args:
            email (EmailField): User Email
            name (CharField): Username
            password (PasswordField): User Password

        Raises:
            ValueError: Raise when no email provided

        Returns:
            User: Created user
        """
        if not email:
            raise ValueError("Email field is required")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, email, name, password):
        """Creates super user

        Args:
            email (EmailField): Super User Email
            name (CharField): Super User Name
            password (PasswordField): Super User Password

        Returns:
            User: Created super user
        """
        user = self.create_user(email=email, name=name, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for system user

    Args:
        AbstractBaseUser (model): Base user provided by django
        PermissionsMixin (mixin): Mixin to modify user permissions (is_superuser or is_staff etc.)
    """
    email = models.EmailField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """String representation of User Model"""
        return self.name

class ProfileFeedItem(models.Model):
    """Profile status update

    Args:
        models (Model): Generic django model
    """
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status_text = models.CharField(max_length=255)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """string representation on profile feed item object

        Returns:
            string: returns status text
        """
        return self.status_text