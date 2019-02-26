from django.urls import path

from . import views

app_name = 'pug_or_ugh'

urlpatterns = [ 
    path('dogs/', views.DogList.as_view(), name='dog_list'),
    path('dogs/<int:pk>', views.DogDetail.as_view(), name='dog_detail')
]