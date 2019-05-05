from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.db.models import ObjectDoesNotExist
from . import models
from . import serializers

# TODO Set up routes
"""
To get the next liked/disliked/undecided dog
GET requests
/api/dog/<pk>/liked/next/
/api/dog/<pk>/disliked/next/
/api/dog/<pk>/undecided/next/
"""

"""
To change the dog' status, 
PUT requests
/api/dog/<pk>/liked/
/api/dog/<pk>/disliked/
/api/dog/<pk>/undecided/
"""

"""
To change a users's preferences
POST requests initially, then a put request
/api/user/preferences/
"""

"""
Notes on Django Token Auth
    When the request is not authenticated, request.user is AnonymousUser, request.auth is None
    When request is authenticated, request.user will be a Django User instance, request.auth will be a rest_framework.authtoken.models.Token instance
"""


class DogList(generics.ListAPIView):
    # permission_classes = (IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class DogDetail(generics.RetrieveAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer



class UserProfile(APIView):
    """Create, Read, and Update currently authenticated user's preferences"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        # since UserPref has a oneToOne relationship with a user it should not allow duplicates
        serializer = serializers.UserPrefSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get(self, request, format=None):
        """Find the users preferences"""
        try:
            user_preferences = models.UserPreference.objects.get(user=request.user)
        except ObjectDoesNotExist:
            raise NotFound
        serializer = serializers.UserPrefSerializer(user_preferences)
        return Response(serializer.data)
    
    def put(self, request, format=None):
        """Update the existing preferences"""
        try:
            user_preferences = models.UserPreference.objects.get(user=request.user)
        except ObjectDoesNotExist:
            raise NotFound
        serializer = serializers.UserPrefSerializer(user_preferences, data=request.data)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data)
