from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # take refernce of Readme file to understand the APIs
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), 
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'), 
    path('api/tasks/create/', views.TaskCreateView.as_view(), name='task-create'),
    path('api/tasks/<int:pk>/assign/', views.TaskAssignView.as_view(), name='task-assign'),
    path('api/users/<int:user_id>/tasks/', views.UserTasksView.as_view(), name='user-tasks'),
    path('api/users/', views.UserListView.as_view(), name='user-list'),
    path('api/users/create/', views.UserCreateView.as_view(), name='user-create'),  
    path('api/users/<int:pk>/', views.UserDetailView.as_view(), name='user-detail'),
]