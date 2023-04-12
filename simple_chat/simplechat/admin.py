from django.contrib import admin
from .models import Thread, Message


@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'updated')
    filter_horizontal = ('participants',)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'thread', 'created', 'is_read')
    list_filter = ('thread', 'created', 'is_read')
    search_fields = ('text', 'sender__username', 'thread__id')