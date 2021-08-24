import logging

from rest_framework import status, viewsets
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.permissions import IsAuthenticated, AllowAny

from . import operations
from . import serializers
from . import models

from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


class AccountViewSet(viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    change_password_serializer_class = serializers.ChangePasswordSerializer
    operations = operations.UserOperations

    def get_object(self, queryset=None):
        if self.request.user:
            return self.request.user
        obj = super().get_object()
        return obj

    def unsubscribe(self, request):
        self.object = self.get_object()
        try:
            count, user = self.operations().delete_user(self.object)
        except Exception as ex:
            logger.error(f"Error while trying to delete the user id {self.object.id}")
            return Response({"response": "There was an error canceling you account"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not count:
            return Response({"response": "Account already cancelled"}, status=status.HTTP_200_OK)
        return Response({"response": "Your account has been canceled correctly"}, status=status.HTTP_200_OK)

    def change_password(self, request):
        self.object = self.get_object()
        serializer = self.change_password_serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({"response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        try:
            self.operations().set_new_password(serializer.validated_data, self.object)
        except Exception as ex:
            logger.error(f"Error while trying to set the new password. Error {str(ex)}")
            return Response({"response": str(ex)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"response": "Password has been changed"},
                        status=status.HTTP_200_OK)

class LoginViewSet(viewsets.GenericViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.LoginSerializer
    authentication_classes = ()
    permission_classes = (AllowAny, )
    user_serializer_class = serializers.UserSerializer

    def login(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': self.user_serializer_class(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_200_OK)


class InsuranceViewSet(viewsets.GenericViewSet):
    queryset = models.Insurance.objects.all()
    serializer_class = serializers.InsuranceSerializer
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (IsAuthenticated, )
    operations = operations.InsuranceOptions
    list_serializer_class = serializers.ListInsuranceSerializer

    def get_queryset(self, pk=None):
        queryset = super().get_queryset()
        if self.request.user:
            queryset = queryset.filter(user=self.request.user)
        if pk:
            queryset = queryset.filter(id=pk)
        return queryset

    def list(self, request):
        queryset = self.get_queryset().values('id', 'insurer__name', 'insurance_category', 'insurance_price')
        serializer = self.list_serializer_class(queryset, many=True)
        return Response({"response": serializer.data}, status=status.HTTP_200_OK)

    def get(self, request, pk):
        queryset = self.get_queryset(pk)
        serializer = self.serializer_class(queryset, many=True)
        return Response({"response": serializer.data}, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data, context=request)
        if not serializer.is_valid():
            return Response({"response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({"response": "The insurance has been created successfully"}, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        try:
            count, items = self.operations().delete_user(pk)
        except Exception as ex:
            logger.error(f"Error while trying to delete the insurance with id {pk}")
            return Response({"response": "There was an error canceling your insurance"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not count:
            return Response({"response": "No insurance deleted"}, status=status.HTTP_200_OK)
        return Response({"response": "The insurance has been deleted successfully"}, status=status.HTTP_200_OK)


class RegisterViewSet(viewsets.GenericViewSet):
    serializer_class = serializers.UserSerializer
    authentication_classes = ()
    permission_classes = (AllowAny, )

    def register(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({"response": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        user, token = serializer.save()
        data = {
            'user': self.serializer_class(user).data,
            'access_token': token
        }
        return Response(data, status=status.HTTP_200_OK)
