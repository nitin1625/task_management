from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Task, User
from .serializers import *


class TaskCreateView(generics.CreateAPIView):
    """Create a new task"""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()

class TaskAssignView(generics.UpdateAPIView):
    """Assign task to users"""
    queryset = Task.objects.all()
    serializer_class = TaskAssignSerializer 
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    
    def update(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(
            task, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class UserTasksView(generics.ListAPIView):
    """Get all tasks for a specific user"""
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        user = get_object_or_404(User, id=user_id)
        return Task.objects.filter(assigned_users=user)
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'user_id': self.kwargs['user_id'],
            'tasks': serializer.data,
            'total_tasks': queryset.count()
        })


class UserCreateView(generics.CreateAPIView):
    """Create a new user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(serializer.validated_data['password'])
        user.save()


class UserListView(generics.ListAPIView):
    """Get all available users"""
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'users': serializer.data,
            'total_users': queryset.count()
        })

class UserDetailView(generics.RetrieveAPIView):
    """Get details of a specific user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'