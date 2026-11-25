from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404
 
from rest_framework.decorators import api_view, permission_classes

from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from rest_framework import status
 
from .models import Project, Task, ProjectMember

from .serializers import (

    ProjectSerializer,

    TaskSerializer,

    ProjectMemberSerializer,

)
 
 
def user_has_project_access(user, project):

    return (

        project.created_by == user

        or ProjectMember.objects.filter(

            project=project,

            user=user

        ).exists()

    )
 
 
def user_is_project_owner(user, project):

    return project.created_by == user or ProjectMember.objects.filter(

        project=project,

        user=user,

        role="Owner"

    ).exists()
 
 
@api_view(["GET", "POST"])

@permission_classes([IsAuthenticated])

def project_list(request):
 
    if request.method == "GET":

        projects = Project.objects.filter(

            models_access_filter(request.user)

        ).distinct()
 
        serializer = ProjectSerializer(projects, many=True)

        return Response(serializer.data)
 
    serializer = ProjectSerializer(data=request.data)
 
    if serializer.is_valid():

        project = serializer.save(created_by=request.user)
 
        ProjectMember.objects.get_or_create(

            project=project,

            user=request.user,

            defaults={"role": "Owner"}

        )
 
        return Response(

            ProjectSerializer(project).data,

            status=status.HTTP_201_CREATED

        )
 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
def models_access_filter(user):

    from django.db.models import Q
 
    return Q(created_by=user) | Q(members__user=user)
 
 
@api_view(["GET", "POST", "DELETE"])

@permission_classes([IsAuthenticated])

def project_members(request, project_id, user_id=None):
 
    project = get_object_or_404(Project, pk=project_id)
 
    if not user_has_project_access(request.user, project):

        return Response(

            {"message": "You do not have access to this project."},

            status=status.HTTP_403_FORBIDDEN

        )
 
    if request.method == "GET":

        members = ProjectMember.objects.filter(project=project)
 
        serializer = ProjectMemberSerializer(members, many=True)

        return Response(serializer.data)
 
    if not user_is_project_owner(request.user, project):

        return Response(

            {"message": "Only project owners can manage members."},

            status=status.HTTP_403_FORBIDDEN

        )
 
    if request.method == "POST":

        username = request.data.get("username")
 
        if not username:

            return Response(

                {"message": "Username is required."},

                status=status.HTTP_400_BAD_REQUEST

            )
 
        user = get_object_or_404(User, username=username)
 
        member, created = ProjectMember.objects.get_or_create(

            project=project,

            user=user,

            defaults={"role": "Member"}

        )
 
        if not created:

            return Response(

                {"message": "User is already a project member."},

                status=status.HTTP_400_BAD_REQUEST

            )
 
        return Response(

            ProjectMemberSerializer(member).data,

            status=status.HTTP_201_CREATED

        )
 
    if request.method == "DELETE":

        if user_id is None:

            return Response(

                {"message": "Member ID is required."},

                status=status.HTTP_400_BAD_REQUEST

            )
 
        member = get_object_or_404(

            ProjectMember,

            project=project,

            user_id=user_id

        )
 
        if member.role == "Owner":

            return Response(

                {"message": "Project owner cannot be removed."},

                status=status.HTTP_400_BAD_REQUEST

            )
 
        member.delete()
 
        return Response(status=status.HTTP_204_NO_CONTENT)
 
 
@api_view(["GET", "POST"])

@permission_classes([IsAuthenticated])

def task_list(request):
 
    if request.method == "GET":

        tasks = Task.objects.filter(

            project__created_by=request.user

        ) | Task.objects.filter(

            project__members__user=request.user

        )
 
        project_id = request.query_params.get("project_id")
 
        if project_id:

            tasks = tasks.filter(project_id=project_id)
 
        tasks = tasks.distinct()
 
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)
 
    project_id = request.data.get("project")
 
    if not project_id:

        return Response(

            {"message": "Project ID is required."},

            status=status.HTTP_400_BAD_REQUEST

        )
 
    project = get_object_or_404(Project, pk=project_id)
 
    if not user_has_project_access(request.user, project):

        return Response(

            {"message": "You do not have access to this project."},

            status=status.HTTP_403_FORBIDDEN

        )
 
    serializer = TaskSerializer(data=request.data)
 
    if serializer.is_valid():

        assigned_user = serializer.validated_data.get("assigned_to")
 
        if assigned_user and not user_has_project_access(

            assigned_user, project

        ):

            return Response(

                {"message": "Assigned user must be a project member."},

                status=status.HTTP_400_BAD_REQUEST

            )
 
        task = serializer.save()
 
        return Response(

            TaskSerializer(task).data,

            status=status.HTTP_201_CREATED

        )
 
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
@api_view(["GET", "PUT", "PATCH", "DELETE"])

@permission_classes([IsAuthenticated])

def task_detail(request, pk):
 
    task = get_object_or_404(Task, pk=pk)

    project = task.project
 
    if not user_has_project_access(request.user, project):

        return Response(

            {"message": "You do not have access to this task."},

            status=status.HTTP_403_FORBIDDEN

        )
 
    if request.method == "GET":

        return Response(TaskSerializer(task).data)
 
    if request.method in ["PUT", "PATCH"]:
 
        serializer = TaskSerializer(

            task,

            data=request.data,

            partial=request.method == "PATCH"

        )
 
        if serializer.is_valid():
 
            updated_project = serializer.validated_data.get(

                "project", task.project

            )
 
            if not user_has_project_access(

                request.user, updated_project

            ):

                return Response(

                    {"message": "You do not have access to that project."},

                    status=status.HTTP_403_FORBIDDEN

                )
 
            assigned_user = serializer.validated_data.get(

                "assigned_to", task.assigned_to

            )
 
            if assigned_user and not user_has_project_access(

                assigned_user, updated_project

            ):

                return Response(

                    {"message": "Assigned user must be a project member."},

                    status=status.HTTP_400_BAD_REQUEST

                )
 
            serializer.save()

            return Response(serializer.data)
 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    if not user_is_project_owner(request.user, project):

        return Response(

            {"message": "Only project owners can delete tasks."},

            status=status.HTTP_403_FORBIDDEN,

        )
 
    task.delete()

    return Response(status=status.HTTP_204_NO_CONTENT)
 
 