
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),

] + i18n_patterns(
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('news.urls')),
    path('users/', include('foydalanuvchilar.urls')),
    path('account/', include('account.urls')),
)



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)