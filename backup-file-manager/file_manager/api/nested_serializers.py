from rest_framework import serializers

from file_manager import models
from utilities.api import WritableNestedSerializer

__all__ = [
    'NestedUploadServerSerializer',
]


class NestedUploadServerSerializer(WritableNestedSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='file-manager-api:site-detail')

    class Meta:
        model = models.UploadServer
        fields = [
            'id', 'name', 'ip_address', 'description', 'slug'
        ]
