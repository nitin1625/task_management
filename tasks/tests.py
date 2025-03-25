from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User, Task, TaskType, TaskAssignment, TaskStatus


class TaskManagementAPITestCase(TestCase):
    """Test cases for the Task Management API"""
    
    def setUp(self):
        """Set up test data"""
        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='password123',
            name='Admin User',
            is_staff=True
        )
        
        self.test_user1 = User.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='password123',
            name='Test User 1'
        )
        
        self.test_user2 = User.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='password123',
            name='Test User 2'
        )
        
        # Create task type
        self.task_type = TaskType.objects.create(
            name='Bug Fix',
            description='Fixing a bug in the system'
        )
        
        # Set up API client and authenticate
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)
        
    def test_create_task(self):
        """Test creating a new task"""
        url = reverse('task-list')
        data = {
            'name': 'Test Task',
            'description': 'This is a test task',
            'task_type': self.task_type.id,
            'status': TaskStatus.PENDING,
            'created_by': self.admin_user.id
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.get().name, 'Test Task')
    
    def test_assign_task(self):
        """Test assigning a task to users"""
        # Create a task first
        task = Task.objects.create(
            name='Assignment Test Task',
            description='Task to be assigned',
            task_type=self.task_type,
            created_by=self.admin_user
        )
        
        url = reverse('taskassignment-assign-task')
        data = {
            'task': task.id,
            'user_ids': [self.test_user1.id, self.test_user2.id]
        }
        
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Check that the task was assigned to both users
        self.assertEqual(task.assigned_users.count(), 2)
        self.assertTrue(task.assigned_users.filter(id=self.test_user1.id).exists())
        self.assertTrue(task.assigned_users.filter(id=self.test_user2.id).exists())
    
    def test_get_user_tasks(self):
        """Test getting tasks for a specific user"""
        # Create and assign tasks
        task1 = Task.objects.create(
            name='User 1 Task',
            description='Task for User 1',
            task_type=self.task_type,
            created_by=self.admin_user
        )
        
        task2 = Task.objects.create(
            name='User 1 and 2 Task',
            description='Task for both users',
            task_type=self.task_type,
            created_by=self.admin_user
        )
        
        # Assign tasks
        TaskAssignment.objects.create(
            task=task1,
            user=self.test_user1,
            assigned_by=self.admin_user
        )
        
        TaskAssignment.objects.create(
            task=task2,
            user=self.test_user1,
            assigned_by=self.admin_user
        )
        
        TaskAssignment.objects.create(
            task=task2,
            user=self.test_user2,
            assigned_by=self.admin_user
        )
        
        # Test fetching User 1 tasks
        url = f"{reverse('task-user-tasks')}?user_id={self.test_user1.id}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
        # Test fetching User 2 tasks
        url = f"{reverse('task-user-tasks')}?user_id={self.test_user2.id}"
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)