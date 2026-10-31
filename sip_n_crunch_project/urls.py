from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
]

# Yeh line production aur local dono mein media pictures show karwayegi
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    # Render (production) par media files serve karne ke liye
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)