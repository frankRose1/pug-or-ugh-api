from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

app_name = 'pug_or_ugh'

urlpatterns = [ 
    path('api/dogs/', views.DogList.as_view(), name='dog_list'),
    path('api/dogs/<int:pk>', views.DogDetail.as_view(), name='dog_detail'),
    path('api/user/login/', obtain_auth_token, name='user_login'),
    path('api/user/preferences', views.UserPref.as_view(), name='user_preferences'),
    path('api/user', views.CreateUser.as_view(), name='create_user'),
    path('api/dog/<int:pk>/liked/next', views.NextLikedDog.as_view(), name='next_liked_dog'),
    path('api/dog/<int:pk>/disliked/next', views.NextDislikedDog.as_view(), name='next_disliked_dog'),
    path('api/dog/<int:pk>/undecided/next', views.NextUndecidedDog.as_view(), name='next_undecided_dog'),
    path('api/dog/<int:pk>/liked', views.LikeDog.as_view(), name='like_dog'),
    path('api/dog/<int:pk>/disliked', views.DislikeDog.as_view(), name='dislike_dog'),
    path('api/dog/<int:pk>/undecided', views.UndecidedDog.as_view(), name='undecided_dog'),
]