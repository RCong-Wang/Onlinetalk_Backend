from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    # 定義一個 FriendSerializer 用於處理 UserProfile 中的 friend 字段
    friend = serializers.PrimaryKeyRelatedField(many=True, queryset=UserProfile.objects.all())

    class Meta:
        model = UserProfile
        fields = ('user', 'friend')  # 需要序列化的字段class UserProfileSerializer(serializers.ModelSerializer):


