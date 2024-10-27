from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('user.urls')),
                  path('', include('common.urls')),
                  path('', include('account.urls')),
                  path('', include('score.urls'))
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
