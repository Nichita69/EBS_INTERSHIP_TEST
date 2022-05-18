from django.urls import path
from rest_framework.routers import DefaultRouter

from task.views import TaskViewSet, CommentViewSet
# from task.views import TaskListView, TaskViewSet
# from task.views import TaskItemPostView
# from task.views import TaskItemView

router = DefaultRouter()
router.register('task', TaskViewSet, basename='task')
router.register('comments', CommentViewSet, basename='comment')
urlpatterns = [
    # path('task/', TaskListView.as_view(), name='task_list'),
    # path('task/create/', TaskItemPostView.as_view(), name='task_list'),
    # path('task/<int:pk>/', TaskItemView.as_view(), name='id_item'),
    *router.urls
]