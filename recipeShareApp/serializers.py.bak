from .models import Message
from rest_framework import serializers


class MessageSerializer(serializers.HyperlinkedModelSerializer):
    photo = serializers.ImageField(use_url=True)

    class Meta:
        model = Message
        #fields = ('first_name', 'last_name', 'image')
        fields = ('user', 'message', 'photo' )