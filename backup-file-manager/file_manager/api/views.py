#
# IP addresses
#
from file_manager import filters
from file_manager.api import serializers
from file_manager.models import UploadServer, BackupFile
from utilities.api import ModelViewSet


class UploadServerViewSet(ModelViewSet):
    queryset = UploadServer.objects.all()
    serializer_class = serializers.UploadServerSerializer
    filterset_class = filters.UploadServerFilter


class BackupFileViewSet(ModelViewSet):
    queryset = BackupFile.objects.all()
    serializer_class = serializers.BackupFileSerializer
    filterset_class = filters.BackupFileFilter
