from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator

# Customer User Model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)


# User Model
class User(AbstractBaseUser, PermissionsMixin):
    DEPARTMENT_CHOICES = (
        ('ENGINEERING', 'Engineering'),
        ('PRODUCT', 'Product'),
        ('SALES', 'Sales'),
        ('MARKETING', 'Marketing'),
        ('HR', 'Human Resources'),
        ('OTHER', 'Other'),
    )
    
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    mobile = models.CharField(max_length=15, blank=True, null=True,validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$', 
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )
        ])
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES, default='OTHER')
    job_title = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-created_at']


# Task Model
class Task(models.Model):
    TASK_TYPES = (
        ('MEETING', 'Meeting'),
        ('DEVELOPMENT', 'Development'),
        ('REVIEW', 'Review'),
        ('RESEARCH', 'Research'),
        ('OTHER', 'Other'),
    )
    
    PRIORITY_LEVELS = (
        ('HIGH', 'High'),
        ('MEDIUM', 'Medium'),
        ('LOW', 'Low'),
    )
    
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    )
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    task_type = models.CharField(max_length=20, choices=TASK_TYPES, default='OTHER')
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    due_date = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    assigned_users = models.ManyToManyField(User, related_name='tasks')
    
    def save(self, *args, **kwargs):
        # Automatically set or clear completed_at based on status
        if self.status == 'COMPLETED' and self.completed_at is None:
            self.completed_at = timezone.now()
        elif self.status != 'COMPLETED' and self.completed_at is not None:
            self.completed_at = None
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['due_date', '-priority', '-created_at']