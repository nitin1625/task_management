from rest_framework import serializers
from .models import Task, User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)  # Added for creation
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'mobile', 
            'department', 'job_title', 'created_at', 
            'last_login', 'password'
        ]
        read_only_fields = ['created_at', 'last_login']

class TaskSerializer(serializers.ModelSerializer):
    assigned_users = UserSerializer(many=True, read_only=True)
    assigned_user_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        many=True,
        write_only=True,
        source='assigned_users'
    )
    
    class Meta:
        model = Task
        fields = [
            'id', 'name', 'description', 'created_at', 
            'task_type', 'priority', 'status', 'due_date',
            'completed_at', 'assigned_users', 'assigned_user_ids'
        ]
        
    def validate(self, data):
        if 'due_date' in data and data['due_date'] < timezone.now():
            raise serializers.ValidationError("Due date cannot be in the past")
        return data