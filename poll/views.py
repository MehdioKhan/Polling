from .models import Poll,PollAnswer,RequestedPoll
from .serializers import PollDetailsSerializer,PollListSerializer,\
    PollAnswerSerializer,RequestedPollCreateSerializer,RequestedPollSerializer
from rest_framework import generics,viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def poll_link_create(request):
    serializer = RequestedPollCreateSerializer(data=request.data)
    if serializer.is_valid():
        obj = serializer.save()
    else:
        obj = RequestedPoll.objects.get(poll=request.data.get('poll'),user=request.data.get('user'))
    link_serializer = RequestedPollSerializer(obj)
    return Response(link_serializer.data)


@api_view(['GET'])
def answer_poll_by_link(request,param):
    from_user = request.user
    try:
        obj=RequestedPoll.objects.get(url_param=param)
    except RequestedPoll.DoesNotExist:
        return Response('Invalid Parameter')
    to_user = obj.user
    poll = obj.poll
    return Response({'poll':poll.id,'from_user':from_user.id,'to_user':to_user.id})