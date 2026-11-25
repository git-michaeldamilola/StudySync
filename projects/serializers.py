from datetime import date
 
from rest_framework import serializers

from .models import Project, Task, ProjectMember
 
 
class ProjectSerializer(serializers.ModelSerializer):

    created_by = serializers.ReadOnlyField(source="created_by.username")

    total_tasks = serializers.SerializerMethodField()

    completed_tasks = serializers.SerializerMethodField()

    progress_percent = serializers.SerializerMethodField()
 
    class Meta:

        model = Project

        fields = "__all__"
 
    def get_total_tasks(self, obj):

        return obj.tasks.count()
 
    def get_completed_tasks(self, obj):

        return obj.tasks.filter(status="Completed").count()
 
    def get_progress_percent(self, obj):

        total = obj.tasks.count()

        if total == 0:

            return 0

        completed = obj.tasks.filter(status="Completed").count()

        return round((completed / total) * 100)
 
 
class TaskSerializer(serializers.ModelSerializer):

    is_overdue = serializers.SerializerMethodField()
 
    class Meta:

        model = Task

        fields = "__all__"
 
    def get_is_overdue(self, obj):

        return (

            obj.due_date is not None

            and obj.due_date < date.today()

            and obj.status != "Completed"

        )
 
 
class ProjectMemberSerializer(serializers.ModelSerializer):

    username = serializers.ReadOnlyField(source="user.username")

    email = serializers.ReadOnlyField(source="user.email")
 
    class Meta:

        model = ProjectMember

        fields = ["id", "user", "username", "email", "role", "joined_at"]
 