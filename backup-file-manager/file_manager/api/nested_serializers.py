from rest_framework import serializers

from file_manager import models
from utilities.api import WritableNestedSerializer

__all__ = [
    'NestedUploadServerSerializer',
]


class NestedUploadServerSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='file-manager-api:backupfile-detail')

    class Meta:
        model = models.UploadServer
        fields = [
            'id', 'url', 'name', 'ip_address', 'description', 'slug'
        ]
