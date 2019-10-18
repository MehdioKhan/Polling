from .models import Poll,PollAnswer,RequestedPoll,Question,Choice,QuestionAnswer
from .serializers import PollDetailsSerializer,PollListSerializer,\
    PollAnswerSerializer,RequestedPollCreateSerializer,RequestedPollSerializer,\
    QuestionSerializer,ChoiceSerializer
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
    serializer = RequestedPollCreateSerializer(data=request.data,context={'request':request})
    if serializer.is_valid():
        obj = serializer.save()
    else:
        if request.data.get('poll') and request.data.get('user'):
            obj = RequestedPoll.objects.get(poll=request.data.get('poll'),user=request.data.get('user'))
        else:
            return Response(serializer.errors)
    link_serializer = RequestedPollSerializer(obj,context={'request':request})
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


def calc(context,user, poll):
    q = Question.objects.filter(answer__to_user=user).distinct()
    result = []
    for x in q.all():
        percents = x.choices_percentage(user,poll)
        answers = []
        for p in percents:
            c = ChoiceSerializer(p[0],context=context)
            answers.append({'choice':c.data,'percentage':p[1]})
        q = QuestionSerializer(x,context=context)
        result.append(
            {'question': q.data, 'answer': answers,'avg':x.average(user,poll)}
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
            res = calc({'request':request},user,obj.pk)
        except Poll.DoesNotExist:
            return Response('Invalid Poll')
    else:
        return Response('Poll Required')
    return Response(res)