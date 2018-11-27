from django.urls import path, include
from django.contrib import admin

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Company-Employee API",
      default_version='v1',
   ),
   public=True,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('swaggeryaml', schema_view.without_ui(cache_timeout=0), name='schema-yaml'),
]
