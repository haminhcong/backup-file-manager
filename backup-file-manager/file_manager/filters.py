import django_filters
from django.db.models import Q

from file_manager.constants import SERVER_TYPE_CHOICES
from file_manager.models import UploadServer, BackupFile


class UploadServerFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    server_type = django_filters.MultipleChoiceFilter(
        choices=SERVER_TYPE_CHOICES,
    )

    class Meta:
        model = UploadServer
        fields = ['name']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
                Q(name__icontains=value) |
                Q(ip_address__istartswith=value)
        )
        return queryset.filter(qs_filter)


class BackupFileFilter(django_filters.FilterSet):
    q = django_filters.CharFilter(
        method='search',
        label='Search',
    )
    upload_server_id = django_filters.ModelMultipleChoiceFilter(
        field_name='upload_server_id',
        queryset=UploadServer.objects.all(),
        label='Upload Server (ID)',
    )
    upload_server = django_filters.ModelMultipleChoiceFilter(
        field_name='upload_server_name',
        queryset=UploadServer.objects.all(),
        label='Upload Server (ID)',
    )

    class Meta:
        model = BackupFile
        fields = ['filename']

    def search(self, queryset, name, value):
        if not value.strip():
            return queryset
        qs_filter = (
                Q(filename__istartswith=value) |
                Q(absolute_file_path__icontains=value)
        )
        return queryset.filter(qs_filter)
