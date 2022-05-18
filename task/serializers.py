from task.models import Task, Comment
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "user", "status")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text", "id", "user", "task")
