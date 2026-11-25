from django.contrib import admin

from .models import Project, Task, ProjectMember
 
 
@admin.register(Project)

class ProjectAdmin(admin.ModelAdmin):

    list_display = ("id", "name", "created_by", "created_at")

    search_fields = ("name", "created_by__username")
 
 
@admin.register(Task)

class TaskAdmin(admin.ModelAdmin):

    list_display = (

        "id",

        "title",

        "project",

        "assigned_to",

        "status",

        "due_date",

    )

    list_filter = ("status", "due_date")

    search_fields = ("title", "project__name")
 
 
@admin.register(ProjectMember)

class ProjectMemberAdmin(admin.ModelAdmin):

    list_display = ("id", "project", "user", "role", "joined_at")

    list_filter = ("role", "project")

    search_fields = ("project__name", "user__username")
 