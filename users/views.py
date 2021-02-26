import logging 

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Team
from .serializers import (
    UserSerializer,
    TeamSerializer,
    ManagementSerializer
)

User = get_user_model()

logger = logging.getLogger("django")

class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
    
class TeamViewset(viewsets.ModelViewSet):
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    
    def destroy(self, request, *args, **kwargs):
        
        group = self.get_object()
        if group.user_set.all():
            logger.info("Trying to delete a not empty group")
            return Response(
                {
                    "message": "Group has users. Can not be deleted."
                },
                status=status.HTTP_400_BAD_REQUEST
            )        
        group.delete()
        logger.info("Group deleted")
        return Response(
                {
                    "message": "Group deleted successfully"
                },
                status=status.HTTP_200_OK
            )
    
    
class AddUserToGroup(APIView):
    def post(self, request, group_id):
        serializer = ManagementSerializer(data=request.data)        
        if serializer.is_valid():
            validated_data = request.data
            user = get_object_or_404(User, id=validated_data["id"])
            group = get_object_or_404(Team, id=group_id)

            user.groups.add(group)
            logger.info(f"Adding user {user.username} to group {group.name}")
            
            return Response(
                {
                    "message": "User added to the group successfully"
                },
                status=status.HTTP_200_OK
            )
            
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )


class RemoveUserFromGroup(APIView):
    def delete(self, request, group_id):
        serializer = ManagementSerializer(data=request.data)        
        if serializer.is_valid():
            validated_data = request.data
            user = get_object_or_404(User, id=validated_data["id"])
            group = get_object_or_404(Team, id=group_id)
            group.user_set.remove(user)
            logger.info(f"Removing user {user.username} from group {group.name}")
            return Response(
                {
                    "message": "User successfully removed from this group"
                },
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
