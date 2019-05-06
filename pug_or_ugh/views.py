from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.db.models import ObjectDoesNotExist
from django.urls import reverse
from django.db.models import Q
from . import models
from . import serializers


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
        headers = {'location': reverse('dogs:user_preferences')}
        try:
            # to send a nicer message to the client
            existing_pref = models.UserPreference.objects.get(user=request.user)
        except ObjectDoesNotExist:
            serializer = serializers.UserPrefSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(
                data='', 
                status=status.HTTP_201_CREATED, 
                headers=headers
            )
        else:
            return Response(
                data={'detail': 'This user has already created their preferences.'},
                status=status.HTTP_400_BAD_REQUEST,
                headers=headers
            )

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
        return Response(
            data='', 
            status=status.HTTP_204_NO_CONTENT,
            headers={'location': reverse('dogs:user_preferences')}
        )


"""
To get the next liked/disliked/undecided dog
GET requests
/api/dog/<pk>/liked/next/
/api/dog/<pk>/disliked/next/
/api/dog/<pk>/undecided/next/
"""
class NextLikedDogView(APIView):
    """
        Retrieves the next dog from the queryset of liked dogs
        :pk: will identify the current dog
    """
    permission_classes=(IsAuthenticated,)

    def get(self, request, pk, format=None):
        dogs = models.Dog.objects.filter(
            Q(userdog__user__id=request.user.id) &
            Q(userdog__status='l') &
            Q(id__gt=pk)
        )
        serializer = serializers.DogSerializer(dogs.first())
        return Response(serializer.data, status=status.HTTP_200_OK)


class NextDogUnliked(APIView):
    """
        Retrieves the next dog from the queryset of unliked dogs
        :pk: will identify the current dog
    """
    pass


class NextDogUndecided(APIView):
    """
        Retrieves the next dog from the queryset of undecided dogs
        :pk: will identify the current dog
    """
    pass

"""
To change the dog' status (UserDog model), 
PUT requests
/api/dog/<pk>/liked/
/api/dog/<pk>/disliked/
/api/dog/<pk>/undecided/
"""