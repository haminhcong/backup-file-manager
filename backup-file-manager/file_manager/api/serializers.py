from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from file_manager.api.nested_serializers import NestedUploadServerSerializer
from file_manager.constants import SERVER_TYPE_CHOICES
from file_manager.models import UploadServer, BackupFile
from utilities.api import ValidatedModelSerializer, ChoiceField


class UploadServerSerializer(ValidatedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='file-manager-api:uploadserver-detail')
    server_type = ChoiceField(choices=SERVER_TYPE_CHOICES, required=False)

    class Meta:
        model = UploadServer
        fields = [
            'id', 'url', 'name', 'ip_address', 'server_type', 'description', 'slug'
        ]


class BackupFileSerializer(ValidatedModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='file-manager-api:backupfile-detail')
    upload_server = PrimaryKeyRelatedField(queryset=UploadServer.objects.all())

    class Meta:
        model = BackupFile
        fields = [
            'id', 'url', 'upload_server', 'absolute_file_path', 'filename', 'uuid', 'file'
        ]
