#
# Forms
#
from django import forms


class BootstrapMixin(forms.BaseForm):
    """
    Add the base Bootstrap CSS classes to form elements.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        exempt_widgets = [
            forms.CheckboxInput, forms.ClearableFileInput, forms.FileInput, forms.RadioSelect
        ]

        for field_name, field in self.fields.items():
            if field.widget.__class__ not in exempt_widgets:
                css = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = ' '.join([css, 'form-control']).strip()
            if field.required and not isinstance(field.widget, forms.FileInput):
                field.widget.attrs['required'] = 'required'
            if 'placeholder' not in field.widget.attrs:
                field.widget.attrs['placeholder'] = field.label


class SelectWithDisabled(forms.Select):
    """
    Modified the stock Select widget to accept choices using a dict() for a label. The dict for each option must include
    'label' (string) and 'disabled' (boolean).
    """
    option_template_name = 'widgets/selectwithdisabled_option.html'


class StaticSelect2(SelectWithDisabled):
    """
    A static content using the Select2 widget

    :param filter_for: (Optional) A dict of chained form fields for which this field is a filter. The key is the
        name of the filter-for field (child field) and the value is the name of the query param filter.
    """

    def __init__(self, filter_for=None, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.attrs['class'] = 'service-select2-static'
        if filter_for:
            for key, value in filter_for.items():
                self.add_filter_for(key, value)

    def add_filter_for(self, name, value):
        """
        Add details for an additional query param in the form of a data-filter-for-* attribute.

        :param name: The name of the query param
        :param value: The value of the query param
        """
        self.attrs['data-filter-for-{}'.format(name)] = value


class StaticSelect2Multiple(StaticSelect2, forms.SelectMultiple):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.attrs['data-multiple'] = 1
