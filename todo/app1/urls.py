from django.urls import path
from . import  views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('register/',views.create_user,name='user_register'),
   
path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

path('forgot-password/',views.forgot_password,name='forgot_password'),
path('forgot-password/<encoded_pk>/<token>',
     views.reset_password ,
     name='reset-password'),


path('change-password/',views.change_password,name='change_password'),

path('todo/',views.todo_list,name='todo_list')
]

