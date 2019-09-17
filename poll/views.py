from .models import Poll,PollAnswer,RequestedPoll,Question,Choice,QuestionAnswer
from .serializers import PollDetailsSerializer,PollListSerializer,\
    PollAnswerSerializer,RequestedPollCreateSerializer,RequestedPollSerializer,\
    PollAnswerDetailsSerializer,ResultSerializer,\
    ResultAnswerSerializer,QuestionSerializer,ChoiceSerializer
from rest_framework import generics,viewsets
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny


class PollList(generics.ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PollListSerializer
    queryset = Poll.objects.all()


class PollDetail(generics.RetrieveAPIView):
    permission_classes = (AllowAny,)
    serializer_class = PollDetailsSerializer
    lookup_field = 'pk'
    queryset = Poll.objects.all()


class PollAnswerView(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = PollAnswerSerializer
    queryset = PollAnswer.objects.all()


@api_view(['POST'])
@permission_classes([IsAuthenticated,])
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
@permission_classes([AllowAny,])
def answer_poll_by_link(request,param):
    try:
        obj = RequestedPoll.objects.get(url_param=param)
    except RequestedPoll.DoesNotExist:
        return Response('Invalid Parameter')
    to_user = obj.user
    poll = obj.poll
    return Response({'poll':poll.id,'to_user':to_user.id})


def calc(user, poll):
    q = Question.objects.filter(answer__to_user=user).distinct()
    result = []
    for x in q.all():
        percents = x.choices_percentage(user,poll)
        temp = []
        for p in percents:
            temp.append({'choice':ChoiceSerializer(p[0]).data,'percentage':p[1]})
        result.append(
            {'question': QuestionSerializer(x).data, 'answer': temp,'avg':x.average(user,poll)}
        )
    return result


@api_view(['GET'])
@permission_classes([IsAuthenticated,])
def get_poll_answers(request):
    user = request.user
    poll = request.GET.get('poll')
    if poll:
        try:
            obj = Poll.objects.get(pk=poll)
            res = calc(user,obj.pk)
            ser = ResultSerializer(data=res,many=True)
            ser.is_valid(raise_exception=True)
        except Poll.DoesNotExist:
            return Response('Invalid Poll')
    else:
        return Response('Poll Required')
    return Response(ser.data)