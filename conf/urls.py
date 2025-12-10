from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('frxapp.urls')), # frxapp ni asosiy sahifa qilib ulaymiz
]

# Quyidagi qism rasmlar (media) va stillar (static) to'g'ri ishlashi uchun kerak
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Agar static fayllar ko'rinmay qolsa, quyidagi qator yordam beradi:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])