from django.contrib.auth import get_user_model
from rest_framework import serializers
from . models import Team

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.StringRelatedField(many=True, read_only=True)

    
    class Meta:
        model = User
        fields = ["id", "username", "email", "groups", "created_at", "updated_at"]
        

class TeamSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    def get_users(self, team):
        users = team.user_set.values_list('username', flat=True)
        return users
    
    class Meta:
        model = Team
        fields = ["id", "name", "users", "created_at", "updated_at"]


class ManagementSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    
    class Meta:
        model = User
        fields = ["id"]


        