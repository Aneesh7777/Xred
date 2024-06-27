from rest_framework.serializers import ModelSerializer
from base.models import Room,User,Topic,Message


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['name']


class RoomSerializer(ModelSerializer):

    topic = TopicSerializer(many=False,read_only=True)
    host = UserSerializer(many=False,read_only=True)
    participants = UserSerializer(many=True,read_only=True)
    class Meta:
        model = Room
        fields = ['id','name','description','topic','host','participants']


class MessageSerializer(ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'user', 'body', 'updated', 'created']


class RoomDetailsSerializer(ModelSerializer):
    topic = TopicSerializer(many=False, read_only=True)
    host = UserSerializer(many=False, read_only=True)
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='message_set')

    class Meta:
        model = Room
        fields = ['id', 'name', 'description', 'topic', 'host', 'participants', 'messages']


class TopicSerializer(ModelSerializer):
    rooms = RoomSerializer(many=True, read_only=True, source='room_set')
    class Meta:
        model = Topic
        fields = ['id','name','rooms']


class TopicDetailSerializer(ModelSerializer):
    rooms = RoomDetailsSerializer(many=True, read_only=True, source='room_set')

    class Meta:
        model = Topic
        fields = ['id','name','rooms']
