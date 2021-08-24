from rest_framework import serializers
from . import models
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import password_validation, authenticate
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):

    def create(self, data):
        user = User(**data)
        user.set_password(data.get("password"))
        user.save()
        token, created = Token.objects.get_or_create(user=user)
        return user, token.key

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password')


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):

        user = authenticate(username=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Las credenciales no son válidas')

        self.context['user'] = user
        return data

    def create(self, data):
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value


class InsuranceSerializer(serializers.ModelSerializer):
    insurer_name = serializers.CharField(required=False, source='insurer.name')
    insurer_phone = serializers.CharField(required=False, source='insurer.phone')

    def create(self, data):
        data["user"] = self.context.user
        super().create(data)
        return data

    class Meta:
        model = models.Insurance
        fields = ('id','insurance_price', 'insurance_category', 'periodicity', 'insurer', 'detail', 'coverage_end',
                  'insurer_name', 'insurer_phone')


class ListInsuranceSerializer(serializers.ModelSerializer):
    insurer = serializers.CharField(source='insurer__name')

    class Meta:
        model = models.Insurance
        fields = ('id', 'insurer', 'insurance_category', 'insurance_price', )

