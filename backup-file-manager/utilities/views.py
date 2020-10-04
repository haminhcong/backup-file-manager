import platform
import sys

from django.conf import settings
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count
from django.http import HttpResponseServerError
from django.shortcuts import get_object_or_404, redirect, render
from django.template import loader
from django.template.exceptions import TemplateDoesNotExist
from django.urls import reverse
from django.utils.html import escape
from django.utils.http import is_safe_url
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import requires_csrf_token
from django.views.defaults import ERROR_500_TEMPLATE_NAME
from django.views.generic import View
from django_tables2 import RequestConfig

from utilities.paginator import EnhancedPaginator
from utilities.utils import csv_format


class GetReturnURLMixin(object):
    """
    Provides logic for determining where a user should be redirected after processing a form.
    """
    default_return_url = None

    def get_return_url(self, request, obj=None):

        # First, see if `return_url` was specified as a query parameter or form data. Use this URL only if it's
        # considered safe.
        query_param = request.GET.get('return_url') or request.POST.get('return_url')
        if query_param and is_safe_url(url=query_param, allowed_hosts=request.get_host()):
            return query_param

        # Next, check if the object being modified (if any) has an absolute URL.
        elif obj is not None and obj.pk and hasattr(obj, 'get_absolute_url'):
            return obj.get_absolute_url()

        # Fall back to the default URL (if specified) for the view.
        elif self.default_return_url is not None:
            return reverse(self.default_return_url)

        # If all else fails, return home. Ideally this should never happen.
        return reverse('home')


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


class ObjectEditView(GetReturnURLMixin, View):
    """
    Create or edit a single object.

    model: The model of the object being edited
    model_form: The form used to create or edit the object
    template_name: The name of the template
    """
    model = None
    model_form = None
    template_name = 'utilities/obj_edit.html'
    required_secrets = None

    def get_object(self, kwargs):
        # Look up object by slug or PK. Return None if neither was provided.
        if 'slug' in kwargs:
            return get_object_or_404(self.model, slug=kwargs['slug'])
        elif 'pk' in kwargs:
            return get_object_or_404(self.model, pk=kwargs['pk'])
        return self.model()

    def alter_obj(self, obj, request, url_args, url_kwargs):
        # Allow views to add extra info to an object before it is processed. For example, a parent object can be defined
        # given some parameter from the request URL.
        return obj

    def get(self, request, *args, **kwargs):

        obj = self.get_object(kwargs)
        obj = self.alter_obj(obj, request, args, kwargs)
        # Parse initial data manually to avoid setting field values as lists
        initial_data = {k: request.GET[k] for k in request.GET}
        form = self.model_form(instance=obj, initial=initial_data)

        return render(request, self.template_name, {
            'obj': obj,
            'obj_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': self.get_return_url(request, obj),
        })

    def post(self, request, *args, **kwargs):

        obj = self.get_object(kwargs)
        obj = self.alter_obj(obj, request, args, kwargs)
        form = self.model_form(request.POST, request.FILES, instance=obj)
        obj_form_valid = form.is_valid()
        if obj_form_valid:
            obj_created = not form.instance.pk
            obj = form.save()
            self.do_extra_job(obj)
            msg = '{} {}'.format(
                'Created' if obj_created else 'Modified',
                self.model._meta.verbose_name
            )
            if hasattr(obj, 'get_absolute_url'):
                msg = '{} <a href="{}">{}</a>'.format(msg, obj.get_absolute_url(), escape(obj))
            else:
                msg = '{} {}'.format(msg, escape(obj))
            messages.success(request, mark_safe(msg))

            if '_addanother' in request.POST:
                return redirect(request.get_full_path())

            return_url = form.cleaned_data.get('return_url')
            if return_url is not None and is_safe_url(url=return_url, allowed_hosts=request.get_host()):
                return redirect(return_url)
            else:
                return redirect(self.get_return_url(request, obj))

        return render(request, self.template_name, {
            'obj': obj,
            'obj_type': self.model._meta.verbose_name,
            'form': form,
            'return_url': self.get_return_url(request, obj),
        })

    def do_extra_job(self, obj):
        pass
