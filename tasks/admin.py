from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Task
from django.utils.html import format_html


# Register User Model
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'department', 'job_title', 'mobile', 
                   'created_at', 'last_login', 'is_staff', 'task_count')
    list_filter = ('department', 'is_staff', 'is_active', 'created_at')
    search_fields = ('username', 'email', 'mobile', 'job_title')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal Info', {'fields': ('mobile', 'department', 'job_title')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'created_at')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username','email', 'password1','password2','mobile', 'department', 'job_title'),
        }),
    )
    
    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Tasks Assigned'


# Register Task Model
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'task_type_colored', 'priority_colored', 'status_colored', 
                   'due_date', 'completed_at', 'created_at', 'assigned_users_list')
    list_filter = ('task_type', 'priority', 'status', 'due_date', 'created_at')
    search_fields = ('name', 'description')
    filter_horizontal = ('assigned_users',)
    date_hierarchy = 'due_date'
    
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        ('Task Details', {
            'fields': ('task_type', 'priority', 'status', 'due_date', 'completed_at')
        }),
        ('Assignments', {'fields': ('assigned_users',)}),
    )
    
    def task_type_colored(self, obj):
        return format_html('<span>{}</span>', obj.task_type)
    task_type_colored.short_description = 'Task Type'
    
    def priority_colored(self, obj):
        colors = {'HIGH': 'red', 'MEDIUM': 'orange', 'LOW': 'green'}
        return format_html(
            '<span style="color: {}">{}</span>',
            colors.get(obj.priority, 'black'),
            obj.priority
        )
    priority_colored.short_description = 'Priority'
    
    def status_colored(self, obj):
        colors = {'PENDING': 'orange', 'IN_PROGRESS': 'blue', 'COMPLETED': 'green'}
        return format_html(
            '<span style="color: {}">{}</span>',
            colors.get(obj.status, 'black'),
            obj.status
        )
    status_colored.short_description = 'Status'
    
    def assigned_users_list(self, obj):
        return ", ".join([user.username for user in obj.assigned_users.all()])
    assigned_users_list.short_description = 'Assigned Users'