from .models import Poll,PollAnswer,RequestedPoll,Question,Choice,QuestionAnswer
from .serializers import PollDetailsSerializer,PollListSerializer,\
    PollAnswerSerializer,RequestedPollCreateSerializer,RequestedPollSerializer,\
    PollAnswerDetailsSerializer,ResultSerializer,ResultAnswerSerializer,QuestionSerializer
from rest_framework import generics,viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny


class PollList(generics.ListAPIView):
    permission_classes = (AllowAny)
    serializer_class = PollListSerializer
    queryset = Poll.objects.all()


class PollDetail(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
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
        if request.data.get('poll') and request.data.get('user'):
            obj = RequestedPoll.objects.get(poll=request.data.get('poll'),user=request.data.get('user'))
        else:
            return Response(serializer.errors)
    link_serializer = RequestedPollSerializer(obj)
    return Response(link_serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def answer_poll_by_link(request,param):
    from_user = request.user
    try:
        obj = RequestedPoll.objects.get(url_param=param)
    except RequestedPoll.DoesNotExist:
        return Response('Invalid Parameter')
    to_user = obj.user
    poll = obj.poll
    return Response({'poll':poll.id,'from_user':from_user.id,'to_user':to_user.id})


def calc(user, poll):
    q = Question.objects.filter(answer__to_user=user).distinct()

    result = []
    for x in q.all():
        percents = x.choices_percentage(user,poll)
        result.append(
            {'question': x.body, 'answer': percents}
        )
    return result


@api_view(['GET'])
def get_poll_answers(request):
    user = request.user
    poll = request.GET.get('poll')
    if poll:
        res = calc(user,int(poll))
        ser = ResultSerializer(data=res,many=True)
        ser.is_valid(raise_exception=True)
    else:
        return Response('Poll Required')
    return Response(ser.data)