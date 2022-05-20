from task.models import Task, Comment
from rest_framework import serializers


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title", "description", "user", "is_completed")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("text", "id", "user", "task")


class AssignTaskToUser(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("user",)


class CreateTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("title", "description")


class ListTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("id", "title")


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("task", "text")
