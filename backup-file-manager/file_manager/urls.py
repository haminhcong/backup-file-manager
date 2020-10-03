from django.urls import path

from . import views

app_name = 'file_manager'
urlpatterns = [

    # VRFs
    path(r'upload-servers/', views.UploadServerListView.as_view(), name='uploadserver_list'),
    path(r'backup-files/', views.BackupFileListView.as_view(), name='backupfile_list'),

]
