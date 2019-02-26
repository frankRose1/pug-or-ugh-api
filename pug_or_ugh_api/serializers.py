from rest_framework import serializers

from . import models

# ALL FIELDS ARE NEEDED EXCEPT user

class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Dog
        fields = (
          'name',
          'breed',
          'age',
          'gender',
          'size'
        )


class UserPrefSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserPref
        fields = (
          'age',
          'size',
          'gender'
        )