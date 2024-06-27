from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room,Topic
from .serializers import RoomSerializer,RoomDetailsSerializer,TopicSerializer,TopicDetailSerializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        'GET /api',
        'GET /api/topics',
        'GET /api/topics/:id',
        'GET /api/rooms',
        'GET /api/rooms/:id',
    ]
    return Response(routes)


@api_view(['GET'])
def getRooms(request):
    room = Room.objects.all()
    serializer = RoomSerializer(room,many=True)
    print(serializer)
    return Response(serializer.data)


@api_view(['GET'])
def getRoom(request,pk):
    room = Room.objects.get(id=pk)
    serializer = RoomDetailsSerializer(room,many=False)
    print(serializer)
    return Response(serializer.data)

@api_view(['GET'])
def getTopics(request):
    topic = Topic.objects.all()
    serializer = TopicSerializer(topic,many=True)
    print(serializer)
    return Response(serializer.data)


@api_view(['GET'])
def getTopic(request,pk):
    topic = Topic.objects.get(id=pk)
    serializer = TopicDetailSerializer(topic,many=False)
    print(serializer)
    return Response(serializer.data)

