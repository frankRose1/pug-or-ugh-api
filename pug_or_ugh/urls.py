from django.urls import path

from . import views

app_name = 'pug_or_ugh'

urlpatterns = [ 
    path('dogs/', views.DogList.as_view(), name='dog_list'),
    path('dogs/<int:pk>', views.DogDetail.as_view(), name='dog_detail'),
    path('users/', views.CreateUser.as_view(), name='create_user'),
    path('user/preferences', views.UserPref.as_view(), name='user_preferences'),
    path('dog/<int:pk>/liked/next', views.NextLikedDog.as_view(), name='next_liked_dog'),
    path('dog/<int:pk>/disliked/next', views.NextDislikedDog.as_view(), name='next_disliked_dog'),
    path('dog/<int:pk>/undecided/next', views.NextUndecidedDog.as_view(), name='next_undecided_dog'),
    path('dog/<int:pk>/liked', views.LikeDog.as_view(), name='like_dog')
]