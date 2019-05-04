from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
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


class DogList(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class DogDetail(generics.RetrieveAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer



class UserProfile(APIView):
    """Create, Read, and Update currently authenticated user's preferences
    """

    def post(self, request, format=None):
        # find the profile
        # if the user has a profile set headers to put 
        pass

    def get(self, request, format=None):
        """Find the users preferences"""
        # TODO get the authetnicated user
        current_user = 1
        user_preferences = models.UserPreference.objects.get(user=current_user)
        serializer = serializers.UserPrefSerializer(user_preferences)
        return Response(serializer.data)
    
    def put(self, request, format=None):
        """Update the existing preferences"""
        pass
