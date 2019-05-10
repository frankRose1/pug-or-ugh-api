from rest_framework import serializers
from django.contrib.auth.models import User
from . import models

FEMALE = 'f'
MALE = 'm'
UNKNOWN = 'u'

SMALL = 's'
MEDIUM = 'm'
LARGE = 'l'
EXTRA_LARGE = 'xl'

LIKE = 'l'
DISLIKE = 'd'
UNDECIDED = 'u'

BABY = 'b'
YOUNG = 'y'
ADULT = 'a'
SENIOR = 's'

# Dog
dog_sizes = [SMALL, MEDIUM, LARGE, EXTRA_LARGE, UNKNOWN]
dog_genders = [FEMALE, MALE, UNKNOWN]


# UserPreferences
userpref_ages = [BABY, YOUNG, ADULT, SENIOR]
userpref_sizes = [SMALL, MEDIUM, LARGE, EXTRA_LARGE]
userpref_genders = [FEMALE, MALE]

# UserDog
userdog_status = [LIKE, DISLIKE, UNDECIDED]


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
    
    def validate_age(self, value):
        err = f'Age must be "{BABY}", "{YOUNG}", "{ADULT}", or "{SENIOR}."'
        if value not in userpref_ages:
            raise serializers.ValidationError(err)
        return value

    def validate_gender(self, value):
        err = f'Preferred gender must be either "{MALE}" or "{FEMALE}".'
        if value not in userpref_genders:
            raise serializers.ValidationError(err)
        return value

    def validate_size(self, value):
        err = f'Size must be "{SMALL}", "{MEDIUM}", "{LARGE}", or "{EXTRA_LARGE}".'
        if value not in userpref_sizes:
            raise serializers.ValidationError(err)
        return value


class UserDogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserDog
        fields = (
          'user',
          'dog',
          'status'
        )

    def update(self, instance, validated_data):
        """Will only need to update the status since the user and dog will never
          change for a given relationship
        """
        instance.status = validated_data['status']
        instance.save()
        return instance

    def validate_status(self, value):
        """Make sure value is either l, d, or u """
        err = f'Status can only be "{LIKE}", "{DISLIKE}", or "{UNDECIDED}".'
        if value not in userdog_status:
            raise serializers.ValidationError(err)
        return value


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
