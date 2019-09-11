from rest_framework import generics,mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import UserSignupSerializer,UserSerializer,\
    UserSignInSerializer,UserProfileSerializer
from rest_framework.authtoken.models import Token
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
)
from .authentication import token_expire_handler, expires_in
from django.contrib.auth import authenticate
from .models import User


@permission_classes([AllowAny])
class UserSignup(generics.CreateAPIView):
    serializer_class = UserSignupSerializer


@api_view(["POST"])
@permission_classes((AllowAny,))  # here we specify permission by default we set IsAuthenticated
def login(request):
    signin_serializer = UserSignInSerializer(data=request.data)
    if not signin_serializer.is_valid():
        return Response(signin_serializer.errors, status=HTTP_400_BAD_REQUEST)

    user = authenticate(
        email=signin_serializer.data['email'].lower(),
        password=signin_serializer.data['password']
    )
    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)

    # TOKEN STUFF
    token, _ = Token.objects.get_or_create(user=user)

    # token_expire_handler will check, if the token is expired it will generate new one
    is_expired, token = token_expire_handler(token)  # The implementation will be described further
    user_serialized = UserSerializer(user)

    return Response({
        'user': user_serialized.data,
        'expires_in': expires_in(token),
        'token': token.key
    }, status=HTTP_200_OK)


def delete_token(user):
    try:
        token = Token.objects.get(user=user)
        token.delete()
    except Token.DoesNotExist:
        pass
    return


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    delete_token(request.user)
    return Response('Logged out')


@api_view(['GET'])
def logged_in_user_details(request):
    user_serializer = UserSerializer(request.user)
    return Response(user_serializer.data)


class UserProfileChange(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return User.objects.filter(pk=self.request.user.pk)
