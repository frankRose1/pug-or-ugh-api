from rest_framework import generics

from . import models
from . import serializers


class DogList(generics.ListAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer


class DogDetail(generics.RetrieveAPIView):
    queryset = models.Dog.objects.all()
    serializer_class = serializers.DogSerializer
