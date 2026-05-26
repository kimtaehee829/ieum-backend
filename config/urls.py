"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.utils import timezone
from config.views import health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check),
    path('api/users/', include('users.urls')),
    path('api/posts/', include('posts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def custom_404_view(request, exception=None):
    return JsonResponse({
        "status": 404,
        "error_code": "NOT_FOUND",
        "message": "요청하신 API 주소를 찾을 수 없습니다.",
        "timestamp": timezone.now().strftime('%Y-%m-%dT%H:%M:%SZ')
    }, status=404)

handler404 = custom_404_view