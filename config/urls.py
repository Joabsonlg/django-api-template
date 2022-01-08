from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import IsAuthenticatedOrReadOnly

urlpatterns = [
    path('', include_docs_urls(title='DJANGO API TEMPLATE', permission_classes=[IsAuthenticatedOrReadOnly,])),
    path('admin/', admin.site.urls),
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
]
