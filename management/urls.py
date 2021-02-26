from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/', include('users.urls', namespace='api')),
    path('admin/', admin.site.urls),
    path("api-token-auth/", obtain_auth_token),
]
