from django.db import models
from django.contrib.auth.models import User


class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    # integer in months
    age = models.IntegerField()
    # "m" for male, "f" for female, "u" for unknown
    gender = models.CharField(max_length=1)
    # "s" for small, "m" for medium, "l" for large, "xl" for extra large, "u" for unknown
    size = models.CharField(max_length=2)


# when a user first clicks like/dislike/undecided it will be a post req
# if they ever change their mind it will be a put, would have to find the row where user_id and dog_id match and then update the status
class UserDog(models.Model):
    user = models.OneToOneField(User, on_delete=)
    dog = models.OneToOneField(Dog)
    # "l" for liked, "d" for dislike, "u" for undecided
    status = models.CharField(max_length=1)


# Will control how the dogs are queried/filtered
class UserPreference(models.Model):
    user = models.OneToOneField(User)
    # "b" for baby, "y" for young, "a" for adult, "s" for senior
    age = models.CharField(max_length=1)
    # "f" for female, "m" for male
    gender = models.CharField(max_length=1)
    # "s" for small, "m" for medium, "l" for large, "xl" for extra large, "u" for unknown 
    size = models.CharField(max_length=2)
