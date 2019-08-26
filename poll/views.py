from .models import Poll
from .serializers import PollDetailsSerializer,PollListSerializer
from rest_framework import generics


class PollList(generics.ListAPIView):
    serializer_class = PollListSerializer
    queryset = Poll.objects.all()


class PollDetail(generics.RetrieveAPIView):
    serializer_class = PollDetailsSerializer
    lookup_field = 'pk'
    queryset = Poll.objects.all()
