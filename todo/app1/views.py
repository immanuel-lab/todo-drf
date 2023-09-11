from rest_framework import status
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import CustomUserSerializer,ForgotPasswordSerailizer,ResetPasswordSerializer,ChangePasswordSerializer,DeleteUserSerializer
from django.contrib.auth import get_user_model
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated



@api_view(['POST'])
def create_user(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        message = "User created successfully."
        return Response({'message':message,'data':serializer.data}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





    
@api_view(['POST'])
def forgot_password(request):
 

    serializer = ForgotPasswordSerailizer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.data["email"]
    User=get_user_model()
    user = User.objects.filter(email=email).first()

    if user:
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)
        reset_url = reverse(
            "reset-password",
            kwargs={"encoded_pk": encoded_pk, "token": token},
        )
        reset_link = f"localhost:8000{reset_url}"

        # send the reset_link as mail to the user.

        return Response(
            {
                "message": f"Your password reset link: {reset_link}"
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {"message": "User doesn't exist"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    


@api_view(['PATCH'])
def  reset_password( request, *args, **kwargs):



 
    serializer = ResetPasswordSerializer(
            data=request.data, context={"kwargs": kwargs}
        )
    serializer.is_valid(raise_exception=True)
    return Response(
            {"message": "Password reset complete"},
            status=status.HTTP_200_OK,
        )


# change password

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer=  ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user=request.user
        old_password = serializer.data.get('old_password')
        if not user.check_password(old_password):
            return Response({'message':'please enter correct password'},status=status.HTTP_400_BAD_REQUEST)
        else:
            new_password=serializer.data.get('new_password')
            user.set_password(new_password)
            user.save()
        return Response({'message':'your password has been changed'},status=status.HTTP_200_OK)


#delete user
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    serializer=DeleteUserSerializer(data=request.data)
    if serializer.is_valid():
        user=request.user
        requested_password = serializer.validated_data.get('password')
        if not user.check_password(requested_password):
            return Response({'message':'please enter the correct password'},status=status.HTTP_400_BAD_REQUEST)
        else:
            user.delete()
            return Response({'message':'user deleted successfully'},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)








# todo
