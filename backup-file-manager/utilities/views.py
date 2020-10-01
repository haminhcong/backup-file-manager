import platform
import sys

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.template import loader
from django.template.exceptions import TemplateDoesNotExist
from django.views.decorators.csrf import requires_csrf_token
from django.views.defaults import ERROR_500_TEMPLATE_NAME
from django.views.generic import View
from django_tables2 import RequestConfig

from utilities.paginator import EnhancedPaginator
from utilities.utils import csv_format


@requires_csrf_token
def server_error(request, template_name=ERROR_500_TEMPLATE_NAME):
    """
    Custom 500 handler to provide additional context when rendering 500.html.
    """
    try:
        template = loader.get_template(template_name)
    except TemplateDoesNotExist:
        return HttpResponseServerError('<h1>Server Error (500)</h1>', content_type='text/html')
    type_, error, traceback = sys.exc_info()

    return HttpResponseServerError(template.render({
        'python_version': platform.python_version(),
        'app_version': settings.VERSION,
        'exception': str(type_),
        'error': error,
    }))


class ObjectListView(View):
    """
    List a series of objects.

    queryset: The queryset of objects to display
    filter: A django-filter FilterSet that is applied to the queryset
    filter_form: The form used to render filter options
    table: The django-tables2 Table used to render the objects list
    template_name: The name of the template
    """
    queryset = None
    filter = None
    filter_form = None
    table = None
    template_name = None

    def queryset_to_csv(self):
        """
        Export the queryset of objects as comma-separated value (CSV), using the model's to_csv() method.
        """
        csv_data = []

        # Start with the column headers
        headers = ','.join(self.queryset.model.csv_headers)
        csv_data.append(headers)

        # Iterate through the queryset appending each object
        for obj in self.queryset:
            data = csv_format(obj.to_csv())
            csv_data.append(data)

        return csv_data

    def queryset_to_xlsx(self):
        """
        Export the queryset of objects as comma-separated value (XLSX),
        using the model's to_csv() method.
        """
        headers = []
        for csv_headers in self.queryset.model.csv_headers:
            headers.append(csv_headers.replace('_', ' ').title())
        csv_data = []
        rows = []
        # Iterate through the queryset appending each object
        for obj in self.queryset:
            rows.append(obj.to_csv())
        return {
            'headers': headers,
            'rows': rows
        }

    def get(self, request):

        model = self.queryset.model
        content_type = ContentType.objects.get_for_model(model)

        if self.filter:
            self.queryset = self.filter(request.GET, self.queryset).qs

        # Provide a hook to tweak the queryset based on the request immediately prior to rendering the object list
        self.queryset = self.alter_queryset(request)

        # Compile user model permissions for access from within the template
        perm_base_name = '{}.{{}}_{}'.format(model._meta.app_label, model._meta.model_name)
        permissions = {p: request.user.has_perm(perm_base_name.format(p)) for p in ['add', 'change', 'delete']}

        # Construct the table based on the user's permissions
        table = self.table(self.queryset)
        if 'pk' in table.base_columns and (permissions['change'] or permissions['delete']):
            table.columns.show('pk')

        # Construct queryset for tags list
        if hasattr(model, 'tags'):
            tags = model.tags.annotate(count=Count('extras_taggeditem_items')).order_by('name')
        else:
            tags = None

        # Apply the request context
        paginate = {
            'paginator_class': EnhancedPaginator,
            'per_page': request.GET.get('per_page', settings.PAGINATE_COUNT)
        }
        RequestConfig(request, paginate).configure(table)

        context = {
            'content_type': content_type,
            'table': table,
            'permissions': permissions,
            'filter_form': self.filter_form(request.GET, label_suffix='') if self.filter_form else None,
            'tags': tags,
        }
        context.update(self.extra_context())

        return render(request, self.template_name, context)

    def alter_queryset(self, request):
        # .all() is necessary to avoid caching queries
        return self.queryset.all()

    def extra_context(self):
        return {}
