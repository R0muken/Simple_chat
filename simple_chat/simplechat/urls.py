from django.urls import path

from .views import ThreadCreateAPIView, ThreadDestroyAPIView, ThreadListAPIView, \
    MessageCreateAPIView, MessageListAPIView, MessageMarkAsReadAPIView, UnreadMessageListAPIView

urlpatterns = [
    path('threads/create/', ThreadCreateAPIView.as_view(), name='thread-create'),
    path('threads/<int:pk>/delete/', ThreadDestroyAPIView.as_view(), name='thread-delete'),
    path('threads/', ThreadListAPIView.as_view(), name='thread-list'),
    path('threads/messages/create/', MessageCreateAPIView.as_view(), name='message-create'),
    path('threads/<int:thread_id>/messages/', MessageListAPIView.as_view(), name='message-list'),
    path('messages/<int:pk>/mark_as_read/', MessageMarkAsReadAPIView.as_view(), name='message-mark-as-read'),
    path('threads/<int:thread_id>/unread-messages/', UnreadMessageListAPIView.as_view(), name='unread-message-list'),
]

