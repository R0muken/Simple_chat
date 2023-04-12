from rest_framework import serializers
from .models import Thread, Message
from django.contrib.auth.models import User


class ThreadSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = Thread
        fields = ['id', 'participants', 'created', 'updated']
        read_only_fields = ['id', 'created', 'updated']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())
    thread = serializers.PrimaryKeyRelatedField(queryset=Thread.objects.all())

    class Meta:
        model = Message
        fields = ['id', 'sender', 'text', 'thread', 'created', 'is_read']
        read_only_fields = ['id', 'created', 'is_read']


class MessageMarkAsReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        exclude = ['id', 'sender', 'text', 'thread', 'created',]

    def update(self, instance, validated_data):
        instance.is_read = True
        instance.save()
        return instance
