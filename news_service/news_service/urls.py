from django.urls import path, include

from django.contrib import admin

urlpatterns = [
    path('news/', include('news.urls')),
    path('admin/', admin.site.urls),
]
