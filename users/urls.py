from django.urls import path, include
from rest_framework import routers
from . views import UserViewset, TeamViewset, AddUserToGroup, RemoveUserFromGroup


router = routers.DefaultRouter()
router.register(r"users", UserViewset, basename="users")
router.register(r"groups", TeamViewset, basename="groups")

app_name = "users"

urlpatterns = [
    path('', include(router.urls)),
    path('groups/<int:group_id>/add-user/', AddUserToGroup.as_view(), name="add-user"),
    path('groups/<int:group_id>/remove-user/', RemoveUserFromGroup.as_view(), name="remove-user"),
]