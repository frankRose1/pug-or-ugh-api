from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Dog, UserPreference

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

# class DogViewTests(APITestCase):

#     def setUp(self):
#         self.dog = Dog.objects.create(**dog)
#         self.dog2 = Dog.objects.create(**dog2)

#     def test_dog_list(self):
#         res = self.client.get(reverse('dogs:dog_list'))
#         self.assertEqual(res.status_code, status.HTTP_200_OK)
#         self.assertIn(self.dog, res.data)
#         self.assertIn(self.dog2, res.data)

#     def test_dog_detail(self):
#         res = self.client.get(reverse('dogs:dog_detail', kwargs={'pk': self.dog.id}))
#         print(res.data)
#         self.assertEqual(res.status_code, status.HTTP_200_OK)


class UserPreferenceViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create(
          username='testUser123',
          email='test.user@gmail.com',
          password='testPassword1'
        )
        Token.objects.create(user=self.user)
        self.token = Token.objects.get(user__username='testUser123')
        UserPreference.objects.create(
          size= 'm',
          gender= 'f',
          age= 'b',
          user=self.user
        )
        # authenticate all reqeusts
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_duplicate_user_preferences(self):
        data = {
          'size': 'm',
          'gender': 'f',
          'age': 'b'
        }
        url = reverse('dogs:user_preferences')
        res = self.client.post(url, data=data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res['Location'], url)
        self.assertEqual(res.data['detail'], 'This user has already created their preferences.')

    def test_get_user_preferences(self):
        res = self.client.get(reverse('dogs:user_preferences'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_update_user_preferences(self):
        updated_data = {
          'size': 'm',
          'gender': 'm',
          'age': 's'
        }
        url = reverse('dogs:user_preferences')
        res = self.client.put(url, data=updated_data)
        self.assertEqual(res.data, '')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
    