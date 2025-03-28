# Generated by Django 4.2.10 on 2025-03-25 08:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_alter_task_options_task_due_date_task_priority_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.CharField(choices=[('ENGINEERING', 'Engineering'), ('PRODUCT', 'Product'), ('SALES', 'Sales'), ('MARKETING', 'Marketing'), ('HR', 'Human Resources'), ('OTHER', 'Other')], default='OTHER', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='job_title',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
