# from  rest_framework.decorators import api_view
# # from .models import CustomUser
# # from .models import Todo
# # from .serializers import TodoSerializer
# from rest_framework import status
# from rest_framework.response import Response
# from .serializers import UserRegisterSerializer
# # Create your views here.

# # # view to register
# @api_view(['POST'])
# def UserRegister(request):
#     serializer =UserRegisterSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'message': 'User registered successfully.'})
#     return Response(serializer.errors, status=400)



# view for todo


# @api_view(['GET', 'POST','DELETE'])
# def todo_view(request,pk):
#     if request.method=='GET':
#         qs=Todo.objects.all()
#         serializer=TodoSerializer(qs,many=True)
#         return Response(serializer.data)
#     if request.method == 'POST':
        
#             serializer=TodoSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data,status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors)
        
#     if request.method=="DELETE":
#         try:
#             item = Todo.objects.get(pk=pk)
#             item.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)

#         except  Todo.DoesNotExist:
#            return Response({"error": "Item not found."}, status=status.HTTP_404_NOT_FOUND)

       

# from rest_framework import status

# from rest_framework import generics, permissions
# from rest_framework.response import Response
# # from knox.models import AuthToken
# from .serializers import UserRegisterSerializer

# # Register API
# class UserRegister(generics.GenericAPIView):
#     serializer_class = UserRegisterSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
        




# from rest_framework import generics
# from .serializers import UserRegistrationSerializer

# class UserRegistrationView(generics.CreateAPIView):
#     serializer_class = UserRegistrationSerializer


# used for registering default user model
# from rest_framework import status
# from rest_framework import generics
# from rest_framework.response import Response
# # from knox.models import AuthToken
# from .serializers import UserRegisterSerializer

# # Register API
# class UserRegister(generics.GenericAPIView):
#     serializer_class = UserRegisterSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)
       



from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CustomUserSerializer
# accounts/views.py
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseBadRequest
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CustomUser

@api_view(['POST'])
def user_register(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        message = "User created successfully.Please verify your email and activate your account"
        return Response({"message": message, "data": serializer.data}, status=201)
    return Response(serializer.errors, status=400)




# to verify email


@api_view(['GET'])
def send_verification_email(request):
    user = request.user
    if not user.is_active:
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = f'Click the link below to activate your account:\n\n' \
                  f'http://{current_site.domain}/activate/' \
                  f'{urlsafe_base64_encode(force_bytes(user.pk)).decode()}/' \
                  f'{default_token_generator.make_token(user)}/'
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        return Response({'message': 'Verification email sent successfully.'})
    else:
        return HttpResponseBadRequest('User is already active.')

@api_view(['GET'])
def activate_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True  # Set is_active to True upon verification
        user.save()
        return Response({'message': 'Account activated successfully.'})
    else:
        return HttpResponseBadRequest('Invalid activation link.')
# urlpatterns = [
#     path('register/', UserRegistrationView.as_view(), name='user-registration'),
#     path('verify/<int:pk>/', UserVerificationView.as_view(), name='user-verification'),
# ]