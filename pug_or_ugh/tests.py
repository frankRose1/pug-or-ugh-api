from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from .models import Dog

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

class DogViewTests(APITestCase):

    def setUp(self):
        self.dog = Dog.objects.create(**dog)
        self.dog2 = Dog.objects.create(**dog2)

    def test_dog_list(self):
        res = self.client.get(reverse('dogs:dog_list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(self.dog, res.data)
        self.assertIn(self.dog2, res.data)

    def test_dog_detail(self):
        res = self.client.get(reverse('dogs:dog_detail', kwargs={'pk': self.dog.id}))
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
    