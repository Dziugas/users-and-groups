from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('users.urls', namespace='api')),
    path('admin/', admin.site.urls),
]
