"""import module that register models"""
from typing import Iterable

from django.contrib import admin

from django_base_integration.models import (
    Profile,
    Subscriber
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Profile Admin panel
    """

    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_superuser",
        "is_staff",
    )

    def get_readonly_fields(self, request, obj=None) -> Iterable:
        if obj is not None:
            return ("password",)
        return super(  # pylint: disable=super-with-arguments
            ProfileAdmin, self
        ).get_readonly_fields(request, obj)


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    """
    Subscriber Admin panel
    """

    list_display = ("profile", "gender", "is_adult")

    def is_adult(self, instance: Subscriber) -> bool | None:
        """
        age is over 18 or not
        @param instance:
        @return: bool
        """
        return instance.is_adult

    is_adult.boolean = True
    is_adult.short_description = "Взрослый"
