from .views import TaskList, TaskDetail, ListList, ListDetail
from django.urls import path

urlpatterns = [
    path('task/', TaskList.as_view()),
    path('task/<int:pk>', TaskDetail.as_view()),
    path('list/', ListList.as_view()),
    path('list/<int:pk>', ListDetail.as_view()),
]