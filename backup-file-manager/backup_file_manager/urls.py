from django.conf import settings
from django.conf.urls import include
from django.urls import path, re_path
from django.views.static import serve
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from backup_file_manager.admin import admin_site
from backup_file_manager.views import APIRootView, StaticMediaFailureView
from file_manager.views import BackupFileListView
from users.views import LoginView, LogoutView

openapi_info = openapi.Info(
    title="Backup File Manager API",
    default_version='v2',
    description="API to access Backup File Manager",
    terms_of_service="Backup File Manager Service",
    license=openapi.License(name="Apache v2 License"),
)

schema_view = get_schema_view(
    openapi_info,
    validators=['flex', 'ssv'],
    public=True,
)

_patterns = [

    # Base views
    path('', BackupFileListView.as_view(), name='home'),

    # Login/logout
    path(r'login/', LoginView.as_view(), name='login'),
    path(r'logout/', LogoutView.as_view(), name='logout'),


    # Apps
    path(r'file-manager/', include('file_manager.urls')),
    path(r'user/', include('users.urls')),

    # API
    path('api/', APIRootView.as_view(), name='api-root'),
    path(r'api/file-manager/', include('file_manager.api.urls')),

    path(r'api/docs/', schema_view.with_ui('swagger'), name='api_docs'),
    path(r'api/redoc/', schema_view.with_ui('redoc'), name='api_redocs'),
    re_path(r'^api/swagger(?P<format>.json|.yaml)$', schema_view.without_ui(), name='schema_swagger'),

    # Serving static media in Django to pipe it through LoginRequiredMiddleware
    path(r'media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),

    # Admin
    path(r'admin/', admin_site.urls),

    # Errors
    path('media-failure/', StaticMediaFailureView.as_view(), name='media_failure'),
]

if settings.DEBUG:
    import debug_toolbar

    _patterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]

if settings.METRICS_ENABLED:
    _patterns += [
        path('', include('django_prometheus.urls')),
    ]

# Prepend BASE_PATH
urlpatterns = [
    path('{}'.format(settings.BASE_PATH), include(_patterns))
]

handler500 = 'utilities.views.server_error'
