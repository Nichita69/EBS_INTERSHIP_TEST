from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework import filters

from config.settings import EMAIL_HOST_USER
from task.models import Task, Comment
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from task.serializers import TaskSerializer, CommentSerializer
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
    permission_classes = (IsAuthenticated, )

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
        return Response(CommentSerializer(comment).data)


class TaskViewSet(ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin, GenericViewSet):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
    permission_classes = [IsAuthenticated, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    @serialize_decorator(TaskSerializer)
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

        return Response(TaskSerializer(task).data)

    @action(detail=False, methods=['get'], url_path='my-tasks')
    def my_tasks(self, request, *args, **kwargs):
        user = request.user
        tasks = Task.objects.filter(user=user)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(detail=False, methods=['get'], url_path='completed-tasks')
    def completed_tasks(self, request, *args, **kwargs):
        tasks = Task.objects.filter(status=True)
        return Response(TaskSerializer(tasks, many=True).data)

    @action(detail=True, methods=['patch'], url_path='complete')
    def complete(self, request, *args, **kwargs):
        task = self.get_object()
        task.status = True
        task.save()
        comments = task.comment_set.all()
        users = []
        for comment in comments:
            users.append(comment.user)
        users = set(users)
        for user in users:
            user.email_user(
                subject='Comennted task',
                message='Hello my name is zuzi',
                from_email=EMAIL_HOST_USER
            )
        return Response(TaskSerializer(task).data)

    @serialize_decorator(TaskSerializer)
    def partial_update(self, request, *args, **kwargs):
        response = super(TaskViewSet, self).partial_update(request, *args, **kwargs)
        task = self.get_object()

        task.user.email_user(
            subject='cum viata omului',
            message='a venit acest task',
            from_email=EMAIL_HOST_USER
        )

        return response


