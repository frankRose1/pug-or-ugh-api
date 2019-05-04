from django.test import TestCase
from rest_framework.test import APIRequestFactory
from django.urls import reverse
from .models import Dog

factory = APIRequestFactory()

dog = {
  "name": "Elsa",
  "image_filename": "dog.jpg",
  "breed": "Husky",
  "age": 2,
  "gender": "f",
  "size": "m"
}

dog2 = {
  "name": "Spot",
  "image_filename": "dog2.jpg",
  "breed": "Golden Lab",
  "age": 15,
  "gender": "f",
  "size": "l"
}

class DogViewTests(TestCase):

    def setUp(self):
        self.dog = Dog.objects.create(**dog)
        self.dog2 = Dog.objects.create(**dog2)

    def test_dog_list(self):
        res = factory.get(reverse('dogs:dog_list'))
        self.assertEqual(res.status_code, 200)