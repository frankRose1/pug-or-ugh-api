from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Dog, UserPreference, UserDog

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

dog3 = {
    "name": "Lucy",
    "image_filename": "dog3.jpg",
    "breed": "Shorthair Pointer",
    "age": 8,
    "gender": "f",
    "size": "m"
}

test_user = {
    'username': 'testUser791',
    'email': 'test.user@gmail.com',
    'password': 'testUserPW!'
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


class CreateUserViewTests(APITestCase):

    def test_create_user(self):
        res = self.client.post(reverse('dogs:create_user'), data=test_user)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)


class UserPreferenceViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(**test_user)
        Token.objects.create(user=self.user)
        self.token = Token.objects.get(user__username=self.user.username)
        UserPreference.objects.create(
          size= 'm',
          gender= 'f',
          age= 'b',
          user=self.user
        )
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        self.url = reverse('dogs:user_preferences')

    def test_duplicate_user_preferences(self):
        data = {
          'size': 'm',
          'gender': 'f',
          'age': 'b'
        }
        res = self.client.post(self.url, data=data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res['Location'], self.url)
        self.assertEqual(res.data['detail'], 'This user has already created their preferences.')

    def test_get_user_preferences(self):
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)

    def test_update_user_preferences(self):
        updated_data = {
          'size': 'm',
          'gender': 'm',
          'age': 's'
        }
        res = self.client.put(self.url, data=updated_data)
        self.assertEqual(res.data, '')
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)


class NextUndecidedDogViewTests(APITestCase):
    """User preferences ask for a medium, female dog with age "b" 
      Both self.dog and self.dog3 meet these preferences.
    """
    def setUp(self):
        self.dog = Dog.objects.create(**dog)
        self.dog2 = Dog.objects.create(**dog2)
        self.dog3 = Dog.objects.create(**dog3)
        self.user = User.objects.create_user(**test_user)
        Token.objects.create(user=self.user)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        UserPreference.objects.create(
          size='m',
          gender='f',
          age='b',
          user=self.user
        )

    def test_correct_next_undecided_dog_1(self):
        """self.dog should be returned since it meets the requirements and it's
          the next dog in the list next dog in the list is determined by the 
          current PK (in this case 0)
        """
        res = self.client.get(reverse('dogs:next_undecided_dog', kwargs={'pk': self.dog.id - 1}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], self.dog.name)
        self.assertEqual(res.data['breed'], self.dog.breed)
        self.assertEqual(res.data['age'], self.dog.age)
        self.assertEqual(res.data['gender'], self.dog.gender)
        self.assertEqual(res.data['image_filename'], self.dog.image_filename)
    

    def test_correct_next_undecided_dog_2(self):
        """self.dog3 should be returned since it meets the requirements and it's
          the next dog in the list next dog in the list is determined by the
          current PK (in this case self.dog.id).
        """
        res = self.client.get(reverse('dogs:next_undecided_dog', kwargs={'pk': self.dog.id}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['name'], self.dog3.name)
        self.assertEqual(res.data['breed'], self.dog3.breed)
        self.assertEqual(res.data['age'], self.dog3.age)
        self.assertEqual(res.data['gender'], self.dog3.gender)
        self.assertEqual(res.data['image_filename'], self.dog3.image_filename)

    def test_no_remaining_undecided_dogs(self):
        """If there are no dogs with an ID greater than the current PK, the API
          should return a 404
        """
        res = self.client.get(reverse('dogs:next_undecided_dog', kwargs={'pk': 15}))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class NextLikedDogViewTests(APITestCase):
    """This view will get the next dog in the queryset that has already been
      liked by the user. The next dog is determined by the <pk> in the url
    """
    def setUp(self):
        self.dog = Dog.objects.create(**dog)
        self.dog2 = Dog.objects.create(**dog2)
        self.user = User.objects.create_user(**test_user)
        Token.objects.create(user=self.user)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        UserDog.objects.create(
            user=self.user,
            dog=self.dog,
            status='l'
        )
        UserDog.objects.create(
            user=self.user,
            dog=self.dog2,
            status='l'
        )

    def test_correct_next_liked_dog_1(self):
        res = self.client.get(reverse('dogs:next_liked_dog', kwargs={'pk': self.dog.id - 1}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], self.dog.id)
        self.assertEqual(res.data['name'], self.dog.name)
        self.assertEqual(res.data['breed'], self.dog.breed)

    def test_correct_next_liked_dog_2(self):
        res = self.client.get(reverse('dogs:next_liked_dog', kwargs={'pk': self.dog.id }))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], self.dog2.id)
        self.assertEqual(res.data['name'], self.dog2.name)
        self.assertEqual(res.data['breed'], self.dog2.breed)

    def test_no_remaining_liked_dogs(self):
        """API should return a 404 if the list of liked dogs has been exhausted"""
        res = self.client.get(reverse('dogs:next_liked_dog', kwargs={'pk': 13}))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class NextDislikedDogViewTests(APITestCase):
    """This view will get the next dog in the queryset that has already been
      disliked by the user. The next dog is determined by the <pk> in the url
    """
    def setUp(self):
        self.dog = Dog.objects.create(**dog)
        self.dog2 = Dog.objects.create(**dog2)
        self.user = User.objects.create_user(**test_user)
        Token.objects.create(user=self.user)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        UserDog.objects.create(
            user=self.user,
            dog=self.dog,
            status='d'
        )
        UserDog.objects.create(
            user=self.user,
            dog=self.dog2,
            status='d'
        )

    def test_correct_next_disliked_dog_1(self):
        res = self.client.get(reverse('dogs:next_disliked_dog', kwargs={'pk': self.dog.id - 1}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], self.dog.id)
        self.assertEqual(res.data['name'], self.dog.name)
        self.assertEqual(res.data['image_filename'], self.dog.image_filename)

    def test_correct_next_disliked_dog_2(self):
        res = self.client.get(reverse('dogs:next_disliked_dog', kwargs={'pk': self.dog.id }))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], self.dog2.id)
        self.assertEqual(res.data['name'], self.dog2.name)
        self.assertEqual(res.data['image_filename'], self.dog2.image_filename)

    def test_no_remaining_disliked_dogs(self):
        """API should return a 404 if the list of disliked dogs has been exhausted"""
        res = self.client.get(reverse('dogs:next_disliked_dog', kwargs={'pk': 20}))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)


class LikeDogViewTests(APITestCase):

    def setUp(self):
        self.dog = Dog.objects.create(**dog)
        self.user = User.objects.create_user(**test_user)
        Token.objects.create(user=self.user)
        self.token = Token.objects.get(user__username=self.user.username)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

    def test_create_like_dog(self):
        res = self.client.put(reverse('dogs:like_dog', kwargs={'pk': self.dog.id}))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UserDog.objects.count(), 1)
        self.assertEqual(res['Location'], reverse('dogs:next_liked_dog', kwargs={'pk': self.dog.id - 1}))

    def test_update_existing_like(self):
        """View should update the existing like from 'd' to 'l'"""
        UserDog.objects.create(user=self.user, dog=self.dog, status='d')
        res = self.client.put(reverse('dogs:like_dog', kwargs={'pk': self.dog.id}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(res['Location'], reverse('dogs:next_liked_dog', kwargs={'pk': self.dog.id - 1}))
        user_dog = UserDog.objects.get(user__id=self.user.id, dog__id=self.dog.id)
        self.assertEqual(user_dog.status, 'l')
    
    def test_dog_not_found(self):
        """View should return a 404 if trying to like a dog that doesnt exist"""
        res = self.client.put(reverse('dogs:like_dog', kwargs={'pk': 15}))
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)