from django.conf import settings
from django.conf.urls import include
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from backup_file_manager.views import HomeView, APIRootView, StaticMediaFailureView

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
    path('', HomeView.as_view(), name='home'),
    # API
    path('api/', APIRootView.as_view(), name='api-root'),

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
