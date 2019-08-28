from .models import Poll,QuestionAnswer
from .serializers import PollDetailsSerializer,PollListSerializer,QuestionAnswerSerializer
from rest_framework import generics,viewsets


class PollList(generics.ListAPIView):
    serializer_class = PollListSerializer
    queryset = Poll.objects.all()


class PollDetail(generics.RetrieveAPIView):
    serializer_class = PollDetailsSerializer
    lookup_field = 'pk'
    queryset = Poll.objects.all()


class QuestionAnswerView(viewsets.ModelViewSet):
    serializer_class = QuestionAnswerSerializer
    queryset = QuestionAnswer.objects.all()