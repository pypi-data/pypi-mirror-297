from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.db import models

from django_base_integration.managers import ProfileManager


class Profile(AbstractUser):
    """
    Profile model
    """

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("password",)

    email = models.EmailField(verbose_name="Почта", unique=True, null=False)
    username = models.CharField(verbose_name="Ник", null=True, blank=True)

    balance = models.FloatField(
        verbose_name="Баланс", default=0.0, blank=True, null=True,
        validators=[MinValueValidator(0.)],
    )

    objects = ProfileManager()

    @property
    def cash(self):
        return self.balance

    @cash.setter
    def cash(self, value):
        if value < 0.:
            raise ValidationError("Balance is below 0")
        self.balance = value

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta data
        """

        verbose_name = "Профиль"
        verbose_name_plural = "Профили"


class Subscriber(models.Model):
    """
    Subscriber model
    """

    GENDERS = (("male", "мужчина"), ("female", "женщина"), ("helicopter", "вертолёт"))
    profile = models.OneToOneField(
        Profile,
        verbose_name="Профиль",
        on_delete=models.CASCADE,
        related_name="subscriber",
    )
    gender = models.CharField(
        choices=GENDERS,
        verbose_name="Гендер",
        default="helicopter",
        max_length=32,
        null=True,
        blank=True,
    )
    age = models.PositiveSmallIntegerField(
        verbose_name="Возраст", blank=True, null=True
    )

    def __str__(self):
        return str(self.profile)

    @property
    def is_adult(self) -> bool:
        """
        age is over 18 or not
        @return: bool
        """
        if isinstance(self.age, int):
            return self.age >= 18
        return None

    class Meta:  # pylint: disable=too-few-public-methods
        """
        Meta data
        """

        verbose_name = "Подписчик"
        verbose_name_plural = "Подписчики"
