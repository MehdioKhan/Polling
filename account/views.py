from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from .serializers import UserSignupSerializer,UserSerializer,UserAuthTokenSerializer
from django.utils import timezone
from rest_framework.authtoken.models import Token


class UserSignup(generics.CreateAPIView):
    serializer_class = UserSignupSerializer


@api_view(['POST'])
@permission_classes([AllowAny,])
def login(request):
    serializer = UserAuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    user.last_login = timezone.now()
    user.save(update_fields=['last_login'])
    token,created = Token.objects.get_or_create(user=user)
    user_serializer = UserSerializer(user)
    return Response({'token':token.key,'user':user_serializer.data})


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