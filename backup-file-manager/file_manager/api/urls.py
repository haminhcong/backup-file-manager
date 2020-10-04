from rest_framework import routers

# from . import views
from file_manager.api import views


class FileManagerRootView(routers.APIRootView):
    """
    Extras API root view
    """
    def get_view_name(self):
        return 'FileManager'


router = routers.DefaultRouter()
router.APIRootView = FileManagerRootView

# Upload Server
router.register(r'upload-servers', views.UploadServerViewSet)

# Backup File
router.register(r'backup-files', views.BackupFileViewSet)


app_name = 'file-manager-api'
urlpatterns = router.urls
