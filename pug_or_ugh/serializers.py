from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

# ALL FIELDS ARE NEEDED EXCEPT user

class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dog
        fields = (
          'id',
          'name',
          'breed',
          'age',
          'image_filename',
          'gender',
          'size'
        )


class UserPrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserPreference
        fields = (
          'age',
          'size',
          'gender',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'