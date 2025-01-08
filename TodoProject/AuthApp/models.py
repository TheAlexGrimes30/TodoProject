from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_admin(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('role', CustomUser.Role.ADMIN)
        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    class Role(models.TextChoices):
        USER = "user", _("User")
        ADMIN = "admin", _("Admin")

    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    password = models.TextField()
    role = models.CharField(choices=Role, default=Role.USER)
    date_created = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    class Meta:
        db_table = "users"
        verbose_name = "user"
        verbose_name_plural = "users"
