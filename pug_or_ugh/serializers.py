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


class UserDogSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        """Will only need to update the status since the user and dog will never
          change for a given relationship
        """
        instance.status = validated_data['status']
        instance.save()
        return instance


    class Meta:
        model = models.UserDog
        fields = (
          'user',
          'dog',
          'status'
        )


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

    class Meta:
        extra_kwargs = {
          'password': {'write_only': True}
        }
        model = User
        fields = '__all__'