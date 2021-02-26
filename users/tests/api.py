from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, force_authenticate
from rest_framework import status
from datetime import datetime
from users.models import User, Team

User = get_user_model()


class TestUsers(APITestCase):
    def setUp(self):
        self.users_url = reverse("users:users-list")
        self.user = User.objects.create(username="tom", password="123456")

    def test_anonymous_cannot_see_users(self):
        response = self.client.get(self.users_url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_auth_user_can_create_user(self):
        self.client.force_authenticate(user=self.user)
        data = {"username": "Petras"}
        
        response = self.client.post(self.users_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "Petras")
        
    def test_user_detail_endpoint_displays_related_groups(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:users-detail", args=(self.user.id,))
        group = Team.objects.create(name="NFQGroup")
        self.user.groups.add(group)
               
        response = self.client.get(url)
        
        self.assertEqual(len((response.data["groups"])), 1)


class GroupTests(APITestCase):
    def setUp(self):
        self.groups_url = reverse("users:groups-list")
        self.user = User.objects.create(username="jerry", password="123456")
        self.group = Team.objects.create(name="TestGroup")

    def test_anonymous_cannot_see_groups(self):
        response = self.client.get(self.groups_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_auth_user_can_create_group(self):
        self.client.force_authenticate(user=self.user)
        data = {"name": "NewGroup"}
        
        response = self.client.post(self.groups_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "NewGroup")
        
    def test_group_detail_endpoint_displays_related_users(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:groups-detail", args=(self.group.id,))
        self.user.groups.add(self.group)
               
        response = self.client.get(url)
        
        self.assertEqual(len((response.data["users"])), 1)
        
    def test_add_user_to_a_group(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:add-user", args=(self.group.id,))
        data = { "id": self.user.id}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], 
                         "User added to the group successfully")
        
    def test_remove_user_from_a_group(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:remove-user", args=(self.group.id,))
        data = { "id": self.user.id}
        
        self.user.groups.add(self.group)
        response = self.client.delete(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], 
                         "User successfully removed from this group")
        
    def test_can_not_delete_full_group(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("users:groups-detail", args=(self.group.id,))
        self.user.groups.add(self.group)
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["message"], "Group has users. Can not be deleted.")
        

