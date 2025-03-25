from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('api/tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('api/tasks/<int:pk>/assign/', views.TaskAssignView.as_view(), name='task-assign'),
    path('api/users/<int:user_id>/tasks/', views.UserTasksView.as_view(), name='user-tasks'),
    path('api/users/', views.UserListView.as_view(), name='user-list'),
    path('api/users/create/', views.UserCreateView.as_view(), name='user-create'),  
    path('api/users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]