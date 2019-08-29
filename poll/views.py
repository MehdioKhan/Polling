from .models import Poll,PollAnswer
from .serializers import PollDetailsSerializer,PollListSerializer,PollAnswerSerializer
from rest_framework import generics,viewsets


class PollList(generics.ListAPIView):
    serializer_class = PollListSerializer
    queryset = Poll.objects.all()


class PollDetail(generics.RetrieveAPIView):
    serializer_class = PollDetailsSerializer
    lookup_field = 'pk'
    queryset = Poll.objects.all()


class PollAnswerView(viewsets.ModelViewSet):
    serializer_class = PollAnswerSerializer
    queryset = PollAnswer.objects.all()