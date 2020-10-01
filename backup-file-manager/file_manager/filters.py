import django_filters
from django.db.models import Q

from file_manager.constants import SERVER_TYPE_CHOICES
from file_manager.models import UploadServer


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

