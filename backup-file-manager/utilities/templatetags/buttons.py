from django import template

register = template.Library()


@register.inclusion_tag('buttons/add.html')
def add_button(url):
    return {'add_url': url}


@register.inclusion_tag('buttons/import.html')
def import_button(url):
    return {'import_url': url}


@register.inclusion_tag('buttons/export.html', takes_context=True)
def export_button(context, content_type=None):
    return {
        'url_params': context['request'].GET,
        'export_templates': None,
    }
