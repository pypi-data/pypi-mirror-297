"""Import modules to work with serializers"""
from abc import abstractmethod
from typing import Dict

from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ValidationError
from django.db.models import Model
from rest_framework.serializers import (
    ModelSerializer,
    ValidationError as SerializerError,
    CharField,
    Serializer
)
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from django_base_integration.models import (
    Profile,
    Subscriber
)


class BaseSerializer(ModelSerializer):  # pylint: disable=too-few-public-methods
    """
    Creates instance of model during initialization
    """

    def __init__(self, context: Dict = None, *args, **kwargs):
        super(BaseSerializer, self).__init__(self, *args, **kwargs)
        if context and (request := context.get("request")):
            instance = self.get_instance(request) if request else None
            self.instance = instance if instance is not None else self._blank()
        else:
            self.instance = None

    def _blank(self) -> Model:
        instance = self.Meta.model()
        for field in set(self.Meta.fields):
            try:
                setattr(instance, field, None)
            except AttributeError:
                pass
            except TypeError:
                pass
        return instance

    @abstractmethod
    def get_instance(self, request) -> Model | None:
        """
        Override this method to specify getting
        instance object for each model serializer
        @param request:
        @return:
        """
        return None

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class"""

        model = Model
        fields = []


class SubscriberSerializer(BaseSerializer):
    """
    Subscriber model serializer
    """

    def get_instance(self, request):
        if hasattr(request.user, "subscriber"):
            subscriber = request.user.subscriber
            return subscriber
        return None

    def create(self, profile: Profile):
        self.instance.profile = profile
        self.instance.save()
        return self.instance

    def delete(self):
        """Delete instance function"""
        self.instance.delete()

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class"""

        model = Subscriber
        fields = (
            "gender",
            "age"
        )
        read_only_fields = fields


class UserSerializer(BaseSerializer):
    """
    User model serializer
    """

    password = CharField(required=True, write_only=True, max_length=128)
    subscriber = SubscriberSerializer(read_only=True)

    def create(self, validated_data):
        try:
            profile = Profile.objects.create_user(**validated_data)
        except ValueError as error:
            raise SerializerError(error) from error

        self.instance = profile
        return profile

    def get_instance(self, request):
        return request.user

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class"""

        model = Profile
        read_only_fields = ("balance", "subscriber")
        fields = (
            "email",
            "password",
            "first_name",
            "last_name",
            "balance",
            "subscriber"
        )


class SubscriberUpdateSerializer(SubscriberSerializer):  # pylint: disable=too-many-ancestors
    """
    Subscribe update serializer
    """

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class"""

        model = Subscriber
        fields = (
            "age",
            "gender"
        )


class UserUpdateSerializer(UserSerializer):  # pylint: disable=too-many-ancestors
    """
    User update serializer
    """

    subscriber = SubscriberUpdateSerializer(required=False)

    def update(self, instance, validated_data):
        try:
            subscriber_data = validated_data.pop("subscriber") if "subscriber" in validated_data else dict()
            if hasattr(instance, "subscriber"):
                for field, value in subscriber_data.items():
                    setattr(instance.subscriber, field, value)
                instance.subscriber.save()
            for field, value in validated_data.items():
                setattr(instance, field, value)
            instance.save()
        except ValidationError as error:
            raise SerializerError(error.message) from error

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class"""

        model = Profile
        fields = (
            "email",
            "first_name",
            "last_name",
            "subscriber"
        )
        read_only_fields = ("email",)


class UserLoginSerializer(Serializer):  # pylint: disable=abstract-method
    """
    User login serializer
    """

    email = CharField(max_length=32, required=True)
    password = CharField(required=True, write_only=True, max_length=128)

    def validate(self, attrs):
        try:
            user = authenticate(self.context["request"], username=attrs.get("email"), password=attrs.get("password"))

            if user is None:
                raise SerializerError("User not found or password is incorrect", 400)
            refresh = RefreshToken.for_user(user)

            if api_settings.UPDATE_LAST_LOGIN:
                update_last_login(None, user)

            return {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }
        except ValidationError as error:
            raise SerializerError(error.message) from error
