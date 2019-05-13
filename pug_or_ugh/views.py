from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.shortcuts import get_object_or_404
from django.db.models import ObjectDoesNotExist
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from . import models
from . import serializers
from .utils import get_desired_age_range


class DogList(generics.ListAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class DogDetail(generics.RetrieveAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class CreateUser(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    model = User
    serializer_class = serializers.UserSerializer


class UserPref(APIView):
    """Create, Read, and Update currently authenticated user's preferences"""
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        headers = {'location': reverse('dogs:user_preferences')}
        data = {
            'user': request.user,
            'size': request.data['size'],
            'age': request.data['age'],
            'gender': request.data['gender']
        }
        try:
            # to send a nicer message to the client
            existing_pref = models.UserPreference.objects.get(user=request.user)
        except ObjectDoesNotExist:
            serializer = serializers.UserPrefSerializer(data=data)
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
        data = {
            'user': request.user,
            'size': request.data['size'],
            'age': request.data['age'],
            'gender': request.data['gender']
        }
        try:
            user_preferences = models.UserPreference.objects.get(user=request.user)
        except ObjectDoesNotExist:
            raise NotFound
        else:
            serializer = serializers.UserPrefSerializer(user_preferences, data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                data='', 
                status=status.HTTP_204_NO_CONTENT,
                headers={'location': reverse('dogs:user_preferences')}
            )


"""
To get the next liked/disliked/undecided Dog
GET requests
"""
# dog/<pk>/liked/next/
class NextLikedDog(APIView):
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

        if dogs.first() is None:
            raise NotFound

        serializer = serializers.DogSerializer(dogs.first())
        return Response(serializer.data, status=status.HTTP_200_OK)


# dog/<pk>/disliked/next/
class NextDislikedDog(APIView):
    """
        Retrieves the next dog from the queryset of unliked dogs
        :pk: will identify the current dog
    """
    permission_classes=(IsAuthenticated,)
    
    def get(self, request, pk, format=None):
        dogs = models.Dog.objects.filter(
            Q(userdog__user__id=request.user.id) &
            Q(userdog__status='d') &
            Q(id__gt=pk)
        )

        if dogs.first() is None:
            raise NotFound
        serializer = serializers.DogSerializer(dogs.first())
        return Response(serializer.data, status=status.HTTP_200_OK)


#  dog/<pk>/undecided/next/
class NextUndecidedDog(APIView):
    """
        Retrieves the next dog from the queryset of undecided dogs
        Will filter out dogs that don't match the user's preferences.
        For example will filter out dogs if they are already liked/disliked,
        and will 

        :pk: will identify the current dog
    """
    permission_classes=(IsAuthenticated,)
    
    def get(self, request, pk, format=None):
        try:
            user_pref = models.UserPreference.objects.get(user_id=request.user.id)
        except ObjectDoesNotExist:
            return Response(
                {'detail': 'User has not set up their preferences yet.'}, 
                status=status.HTTP_400_BAD_REQUEST,
                headers={'location': reverse('dogs:user_preferences')}
            )
        dogs = models.Dog.objects.exclude(
            Q(userdog__status__in=('d', 'l')) &
            Q(userdog__user__id=request.user.id)
        ).filter(
            age__in=get_desired_age_range(user_pref_age=user_pref.age),
            gender=user_pref.gender,
            size=user_pref.size,
            id__gt=pk
        ).order_by('pk')

        if dogs.first() is None:
            raise NotFound
        serializer = serializers.DogSerializer(dogs.first())
        return Response(serializer.data, status=status.HTTP_200_OK)


"""
To change the dog' status (UserDog model)
PUT requests
"""
def update_or_create_userdog(dog, user, new_status, headers):
    """LikeDog, DislikeDog, and UndecidedDog each allow a user to create or update
        a UserDog relationship. This function will either create the relationship
        if it doesn't already exist or update the existing relationship

        :dog: - dog object being liked

        :user: - currently authenticated user

        :status: - l(like), d(dislike), or u(undecided)

        :headers: - dict of response headers, such as location
    """
    data = {
        'dog': dog.id,
        'user': user.id,
        'status': new_status
    }
    try:
        # see if a UserDog relationship exists for this user/dog pair
        user_dog = models.UserDog.objects.get(user__id=user.id, dog__id=dog.id)
    except ObjectDoesNotExist:
        # if not create the relationship
        serializer = serializers.UserDogSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('', status=status.HTTP_201_CREATED, headers=headers)
    else:
        # else update the existing relationship
        serializer = serializers.UserDogSerializer(user_dog, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('', status=status.HTTP_204_NO_CONTENT, headers=headers)


# /api/dog/<pk>/liked/
class LikeDog(APIView):
    """Allows a user to like a dog byby creating or updating a UserDog model.
        Sets the status to "l"

        :pk: dog being liked
    """
    permission_classes = (IsAuthenticated,)
    def put(self, request, pk, format=None):
        dog = get_object_or_404(models.Dog, id=pk)
        headers = {'location': reverse('dogs:next_liked_dog', kwargs={'pk': dog.id - 1})}
        return update_or_create_userdog(
                dog=dog, 
                user=request.user, 
                new_status='l', 
                headers=headers
            )



# /api/dog/<pk>/disliked/
class DislikeDog(APIView):
    """Allows a user to dislike a dog by creating or updating a UserDog model.
        Sets the status to "d"

        :pk: dog being disliked
    """
    permission_classes=(IsAuthenticated,)
    def put(self, request, pk, format=None):
        dog = get_object_or_404(models.Dog, id=pk)
        headers = {'location': reverse('dogs:next_disliked_dog', kwargs={'pk': dog.id - 1})}
        return update_or_create_userdog(
                dog=dog, 
                user=request.user, 
                new_status='d', 
                headers=headers
            )


# /api/dog/<pk>/undecided/
class UndecidedDog(APIView):
    """Allows a user to det a dog to undecided by creating or updating a 
        UserDog model. Sets the status to "u"

        :pk: dog
    """
    permission_classes=(IsAuthenticated,)

    def put(self, request, pk, format=None):
        dog = get_object_or_404(models.Dog, id=pk)
        headers = {'location': reverse('dogs:next_undecided_dog', kwargs={'pk': dog.id - 1})}
        return update_or_create_userdog(
                dog=dog, 
                user=request.user, 
                new_status='u', 
                headers=headers
            )
