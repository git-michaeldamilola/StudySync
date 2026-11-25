from django.urls import path

from . import views
 
urlpatterns = [

    path("", views.project_list, name="project-list"),
 
    path(

        "<int:project_id>/members/",

        views.project_members,

        name="project-members"

    ),
 
    path(

        "<int:project_id>/members/<int:user_id>/",

        views.project_members,

        name="project-member-delete"

    ),
 
    path("tasks/", views.task_list, name="task-list"),
 
    path(

        "tasks/<int:pk>/",

        views.task_detail,

        name="task-detail"

    ),

]
 