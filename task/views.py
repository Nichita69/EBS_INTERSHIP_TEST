from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.serializers import Serializer
from rest_framework.status import HTTP_200_OK
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters

from config.settings import EMAIL_HOST_USER
from task.models import Task, Comment
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from task.serializers import TaskSerializer, CommentSerializer, AssignTaskToUser, CreateTaskSerializer, \
    ListTaskSerializer, CreateCommentSerializer
from django.shortcuts import get_object_or_404


# class TaskListView(ListAPIView, GenericAPIView):
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Task.objects.all()


# class TaskItemPostView(GenericAPIView):
#     serializer_class = TaskSerializer
#     permission_classes = [IsAuthenticated]
#     queryset = Task.objects.all()
#
#     @serialize_decorator(TaskSerializer)
#     def post(self, request):
#         validated_data = request.serializer.validated_data
#
#         task = Task.objects.create(
#             title=validated_data['title'],
#             description=validated_data['description'],
#             user=request.user
#         )
#
#         return Response(TaskSerializer(task).data)

#
# class TaskItemView(GenericAPIView):
#     serializer_class = TaskSerializer
#
#     permission_classes = (AllowAny,)
#     authentication_classes = ()
#
#     def get(self, request, pk):
#         task = get_object_or_404(Task.objects.filter(pk=pk))
#
#         return Response(TaskSerializer(task).data)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "create":
            return CreateCommentSerializer
        else:
            return super(CommentViewSet, self).get_serializer_class()


    @serialize_decorator(CommentSerializer)
    def create(self, request, *args, **kwargs):
        validated_data = request.serializer.validated_data
        user = request.user

        comment = Comment.objects.create(
            text=validated_data['text'],
            task=validated_data['task'],
            user=user,
        )

        comment.task.user.email_user(
            subject='Copac',
            message='Trebuesahranimcopaci',
            from_email=EMAIL_HOST_USER
        )
        return Response(comment.id)


class TaskViewSet(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def get_serializer_class(self):
        if self.action == "create":
            return CreateTaskSerializer
        elif self.action == "list":
            return ListTaskSerializer
        else:
            return super(TaskViewSet, self).get_serializer_class()

    @serialize_decorator(CreateTaskSerializer)
    def create(self, request):
        validated_data = request.serializer.validated_data

        user = request.user

        task = Task.objects.create(
            title=validated_data['title'],
            description=validated_data['description'],
            user=user,
        )

        user.email_user(
            subject='ghfgh',
            message='hdh',
            from_email=EMAIL_HOST_USER
        )

        return Response(task.id)

    @action(detail=False, methods=['get'], url_path='my-tasks')
    def my_tasks(self, request, *args, **kwargs):
        user = request.user
        tasks = Task.objects.filter(user=user)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(detail=True, methods=['patch'], serializer_class=AssignTaskToUser, url_path='assign-task-to-user')
    def assign_task_to_user(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        user = User.objects.get(id=validated_data["user"].id)
        task.user = user
        task.save()
        user.email_user(
            subject='Noroc taska bila naznacina you',
            message='githup hello',
            from_email=EMAIL_HOST_USER
        )
        return Response(TaskSerializer(task).data)

    @action(detail=False, methods=['get'], url_path='completed-tasks')
    def completed_tasks(self, request, *args, **kwargs):
        tasks = Task.objects.filter(is_completed=True)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(detail=True, methods=['patch'], serializer_class=Serializer, url_path='complete')
    def complete(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_completed = True
        task.save()

        users = User.objects.filter(comment__task_id=task.id).distinct()

        for user in users:
            user.email_user(
                subject='Comennted task',
                message='Hello my name is zuzi',
                from_email=EMAIL_HOST_USER
            )

        return Response({"status": HTTP_200_OK})

    @action(detail=True, methods=['get'], serializer_class=Serializer, url_path="task_comments")
    def task_comments(self, request, *args, **kwargs):
        task = self.get_object()
        comments = Comment.objects.filter(task=task)
        return Response(CommentSerializer(comments, many=True).data)
