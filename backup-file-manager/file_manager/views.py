#
# IP addresses
#
from django.contrib.auth.mixins import PermissionRequiredMixin

from file_manager import filters, forms, tables
from file_manager.models import UploadServer, BackupFile
from utilities.views import ObjectListView, ObjectEditView


class UploadServerListView(PermissionRequiredMixin, ObjectListView):
    permission_required = 'file_manager.view_uploadserver'
    queryset = UploadServer.objects.all()
    filter = filters.UploadServerFilter
    filter_form = forms.UploadServerFilterForm
    table = tables.UploadServerTable
    template_name = 'file_manager/uploadserver_list.html'


class BackupFileListView(PermissionRequiredMixin, ObjectListView):
    permission_required = 'file_manager.view_backupfile'
    queryset = BackupFile.objects.all()
    filter = filters.BackupFileFilter
    filter_form = forms.BackupFileFilterForm
    table = tables.BackupFileTable
    template_name = 'file_manager/backupfile_list.html'


class BackupFileCreateView(PermissionRequiredMixin, ObjectEditView):
    permission_required = 'file_manager.add_backupfile'
    model = BackupFile
    model_form = forms.BackupFileForm
    default_return_url = 'file_manager:backupfile_list'
