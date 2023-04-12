from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer, MessageMarkAsReadSerializer


class MessageCreateAPIView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Message.objects.all()

    def create(self, request, *args, **kwargs):
        thread_id = request.data.get('thread', None)
        if thread_id is None:
            raise ValidationError('Thread ID is required.')

        thread = Thread.objects.filter(pk=thread_id).filter(participants=request.user).first()
        if thread is None:
            raise ValidationError('You are not a participant.')

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(sender=request.user, thread=thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        thread_id = self.kwargs['thread_id']
        thread = Thread.objects.filter(pk=thread_id).filter(participants=self.request.user).first()
        if thread is None:
            raise ValidationError('You are not a participant.')

        return Message.objects.filter(thread=thread)


class UnreadMessageListAPIView(generics.ListAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        thread_id = self.kwargs['thread_id']
        thread = Thread.objects.filter(pk=thread_id).filter(participants=self.request.user).first()
        if thread is None:
            raise ValidationError('You are not a participant.')

        return Message.objects.filter(thread=thread, is_read=False)


class MessageMarkAsReadAPIView(generics.UpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageMarkAsReadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        message_id = kwargs['pk']

        if not message_id:
            return Response({'error': 'message_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        message = Message.objects.get(id=message_id)
        sender = message.sender
        participants = message.thread.participants.all()

        if sender in participants.exclude(pk=request.user.pk) and participants.exclude(pk=request.user.pk).count() != 2:
            message.is_read = True
            message.save()
        else:
            raise ValidationError('You are not a recipient of this message.')

        return Response(self.get_serializer(message).data)


class ThreadCreateAPIView(generics.CreateAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Thread.objects.all()

    def create(self, request, *args, **kwargs):
        participant_ids = request.data.get('participants', [])
        if len(participant_ids) != 2:
            raise ValidationError('Thread can’t have more than 2 participants.')

        participants = User.objects.filter(id__in=participant_ids)
        if participants.count() != 2:
            raise ValidationError('Invalid IDs.')

        thread = Thread.objects.filter(participants=participants[0]).filter(participants=participants[1]).first()
        if thread is not None:
            serializer = self.get_serializer(thread)
            return Response(serializer.data, status=status.HTTP_200_OK)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ThreadDestroyAPIView(generics.DestroyAPIView):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]


class ThreadListAPIView(generics.ListAPIView):
    serializer_class = ThreadSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Thread.objects.filter(participants=self.request.user)
