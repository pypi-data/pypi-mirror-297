"""Import modules that work with views"""
from typing import Dict

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer

from rest_framework.status import (
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_200_OK,
    HTTP_201_CREATED
)
from rest_framework.response import Response

from django_base_integration.permissions import (
    UnauthenticatedPost,
    AuthenticatedPost,
    SubscribePermission
)
from django_base_integration.serializers import (
    UserSerializer,
    SubscriberSerializer,
    UserUpdateSerializer
)


class RestApi(type):
    """
    Rest api arhitecture
    """

    serializer_class = ModelSerializer
    __methods__ = ["get", "post", "put", "delete"]

    def __new__(mcs, name, bases, kwargs):
        for attr_name in kwargs.get("__methods__", mcs.__methods__):
            if not kwargs.get(attr_name):
                kwargs[attr_name] = getattr(mcs, attr_name)
        if not kwargs.get("get_serializer_context"):
            kwargs["get_serializer_context"] = mcs.get_serializer_context
        if not kwargs.get("get_serializer"):
            kwargs["get_serializer"] = mcs.get_serializer

        return super(RestApi, mcs).__new__(mcs, name, bases, kwargs)

    def get_serializer_context(cls) -> Dict:
        """
        Get serializer context
        @return:
        """
        return {
            "request": getattr(cls, "request"),
            "format": getattr(cls, "format_kwarg"),
            "view": cls,
        }

    def get_serializer(
            cls, *args, **kwargs
    ) -> ModelSerializer:  # pylint: disable=no-value-for-parameter
        """
        Get serializer with context
        @param args:
        @param kwargs:
        @return:
        """
        kwargs[
            "context"
        ] = cls.get_serializer_context()  # pylint: disable=no-value-for-parameter
        return cls.serializer_class(*args, **kwargs)

    def get(
            self, request, **kwargs
    ):  # pylint: disable=unused-argument, bad-mcs-method-argument
        serializer = self.get_serializer()
        return Response(serializer.data, status=HTTP_200_OK)

    def post(self, request, **kwargs):  # pylint: disable=bad-mcs-method-argument
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(serializer.validated_data)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):  # pylint: disable=bad-mcs-method-argument
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.update(serializer.instance, serializer.validated_data)
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(
            self, request, **kwargs
    ):  # pylint: disable=bad-mcs-method-argument, unused-argument
        serializer = self.get_serializer()
        serializer.delete()  # pylint: disable=no-member
        return Response(status=HTTP_204_NO_CONTENT)


"""
Client APIs - available for any telegram user
"""


class UserApi(generics.GenericAPIView, metaclass=RestApi):
    """
    User api
    """

    __methods__ = ["get", "post", "put"]
    serializer_class = UserSerializer
    update_serializer = UserUpdateSerializer
    permission_classes = (IsAuthenticated | UnauthenticatedPost,)

    def get_serializer(self, *args, **kwargs):
        kwargs["context"] = self.get_serializer_context()
        if kwargs["context"]["request"].method == "PUT":
            return self.update_serializer(*args, **kwargs)
        return self.serializer_class(*args, **kwargs)


class SubscriberApi(generics.GenericAPIView, metaclass=RestApi):
    """
    Subscriber api
    """

    __methods__ = ["post", "delete"]
    serializer_class = SubscriberSerializer
    permission_classes = (SubscribePermission | AuthenticatedPost,)

    def post(self, request, **kwargs):  # pylint: disable=bad-mcs-method-argument
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.create(profile=request.user)
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


"""
Admin APIs - available for staff (only)
"""
