from rest_framework import serializers
from .services import UserDataClass
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.Serializer):
     id = serializers.IntegerField(read_only=True)
     first_name = serializers.CharField()
     last_name = serializers.CharField()
     country = serializers.CharField()
     email = serializers.CharField()
     password = serializers.CharField(write_only=True)
     username = serializers.CharField()

     def to_internal_value(self, data):
          data = super().to_internal_value(data)
          return UserDataClass(**data)

     # these tow are used when the serializer calls the .is_valid

     def validate_username(self, value):
          if User.objects.filter(username=value).exists():
               raise serializers.ValidationError("Username already exists")
          return value

     def validate_email(self, value):
          if User.objects.filter(email=value).exists():
               raise serializers.ValidationError("Email already exists")
          return value


