from rest_framework import serializers
from main.models import Employee, Post
from django.contrib.auth.models import User
from rest_framework.authtoken.views import Token
from rest_framework.exceptions import ValidationError


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password',
                  'email', 'first_name', 'last_name']

        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'email': {
                'required': True,
                'allow_blank': False
            },
            'first_name': {
                'required': True,
                'allow_blank': False
            },
            'last_name': {
                'required': True,
                'allow_blank': False
            },
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.get_or_create(user=user)
        return user


class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = "__all__"
        depth = 1

    def create(self, validated_data):
        if validated_data['designation'] != "Default":
            user_instance = UserSerializer.create(
                self, validated_data=validated_data['user'])
            validated_data.pop('user')
            validated_data['user'] = user_instance
            instance = super().create(validated_data)
            return instance
        else:
            raise ValidationError(
                {"designation": ["This field may not be blank."]})


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        extra_kwargs = {
            'date': {
                'read_only': True
            }
        }
