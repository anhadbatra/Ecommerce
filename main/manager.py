from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class CustomUserModel(BaseUserManager):
    def create_user(self,email,password=None,**kwargs):
        email = self.normalize_email(email)
        user = self.model(email=email,**kwargs)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self,email,password,**kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if kwargs.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **kwargs)