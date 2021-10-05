from django.contrib import admin
from django.urls import path,include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from users import users_urls
from app import app_urls
from notification import noti_urls
schema_view = get_schema_view(
    openapi.Info(
        title="Core API",
        default_version='v1',
        description="",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="contact@expenses.local"),
        license=openapi.License(name="Test License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include(users_urls)),
    path('app/', include(app_urls)),
    path('notification/', include(noti_urls)),
    path('', schema_view.with_ui('swagger',cache_timeout=0), name='schema-swagger-ui'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)