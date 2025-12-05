from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frxapp.urls')),
    # frxapp index sahifani default qiladi
]
