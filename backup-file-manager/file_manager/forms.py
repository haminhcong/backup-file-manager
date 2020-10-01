from django import forms

from file_manager.models import UploadServer
from utilities.forms import BootstrapMixin


class UploadServerFilterForm(BootstrapMixin, forms.Form):
    model = UploadServer
    q = forms.CharField(
        required=False,
        label='Search'
    )
