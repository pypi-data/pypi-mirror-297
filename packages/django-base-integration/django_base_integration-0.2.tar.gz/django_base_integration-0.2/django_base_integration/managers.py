"""Import base user manager module"""
from django.contrib.auth.models import UserManager


class ProfileManager(UserManager):
    """
    Profile manager
    """

    def create_user(self, email=None, password=None, **extra_fields):
        if not (email and password):
            raise ValueError("You must specify both telegram_id and chat_id to proceed")
        if extra_fields.get("balance"):
            raise ValueError("You must not provide balance during user creation")

        profile = self.model(email=email, **extra_fields)
        profile.set_password(password)

        profile.save()
        return profile

    def create_superuser(self, email=None, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)
