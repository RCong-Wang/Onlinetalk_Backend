from rest_framework import serializers
from .models import Chatroom, Message
from user.models import UserProfile
from django.contrib.auth.models import User


class ChatroomSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(queryset=UserProfile.objects.all(), many=True)

    class Meta:
        model = Chatroom
        fields = "__all__"
    


class MessageSeralizer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Chatroom.objects.all(), many=True)

    class Meta:
        model = Message
        fields = "__all__"
    
    #將使用者id替換成使用者名稱
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        senter_representation = instance.senter.user.username  # 尋找使用者名稱
        representation['senter'] = senter_representation
        return representation
    
    def validate(self, data):
        senter = data.get('senter')
        if not senter and 'request' in self.context:
            data['senter'] = self.context['request'].user.userprofile

        return data
