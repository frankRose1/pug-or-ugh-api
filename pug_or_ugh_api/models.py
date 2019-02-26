from django.db import models

class Dog(models.Model):
    name = models.CharField(max_length=255)
    # integer in months
    age = models.IntegerField()
    breed = models.CharField(max_length=255)
    # "m" for male, "f" for female, "u" for unknown
    gender = models.CharField(max_length=1)
    # "s" for small, "m" for medium, "l" for large, "xl" for extra large, "u" for unknown
    size = models.CharField(max_length=2)

class UserDog(models.Model):
    pass


class UserPref(models.Model):
    # user = 
    # "b" for baby, "y" for young, "a" for adult, "s" for senior
    age = models.CharField(max_length=1)
    # "f" for female, "m" for male
    gender = models.CharField(max_length=1)
    # "s" for small, "m" for medium, "l" for large, "xl" for extra large, "u" for unknown 
    size = models.CharField(max_length=2)