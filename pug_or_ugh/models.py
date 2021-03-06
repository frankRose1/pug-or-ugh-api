from django.db import models
from django.contrib.auth.models import User

# The first element in each tuple is the actual value to be stored, and the second element is the human-readable name.
# gender
FEMALE = 'f'
MALE = 'm'
UNKNOWN = 'u'
DOG_GENDER_CHOICES = [(FEMALE, 'Female'), (MALE, 'Male'), (UNKNOWN, 'Unknown')]
USER_PREF_GENDER_CHOICES = [(FEMALE, 'Female'), (MALE, 'Male')]

# sizes
SMALL = 's'
MEDIUM = 'm'
LARGE = 'l'
EXTRA_LARGE = 'xl'
SIZE_CHOICES = [(SMALL, 'Small'), (MEDIUM, 'Medium'), (LARGE, 'Large'), (EXTRA_LARGE, 'Extra Large'), (UNKNOWN, 'Unknown')]

# status (UserDog model)
LIKE = 'l'
DISLIKE = 'd'
UNDECIDED = 'u'
STATUS_CHOICES = [(LIKE, 'Like'), (DISLIKE, 'Dislike'), (UNDECIDED, 'Undecided')]

# age (UserPreference model)
BABY = 'b'
YOUNG = 'y'
ADULT = 'a'
SENIOR = 's'
AGE_CHOICES = [(BABY, 'Baby'), (YOUNG, 'Young'), (ADULT, 'Adult'), (SENIOR, 'Senior')]

class Dog(models.Model):
    name = models.CharField(max_length=255)
    image_filename = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField() # integer in months
    gender = models.CharField(max_length=1, choices=DOG_GENDER_CHOICES)
    size = models.CharField(max_length=2, choices=SIZE_CHOICES)


class UserDog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)
    status = models.CharField(max_length=1)


class UserPreference(models.Model):
    """Will control how the dogs are queried/filtered"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.CharField(max_length=1)
    gender = models.CharField(max_length=1)
    size = models.CharField(max_length=2)
