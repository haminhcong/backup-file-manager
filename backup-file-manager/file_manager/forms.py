from django import forms

from file_manager.models import UploadServer, BackupFile
from utilities.forms import BootstrapMixin, StaticSelect2


class UploadServerFilterForm(BootstrapMixin, forms.Form):
    model = UploadServer
    q = forms.CharField(
        required=False,
        label='Search'
    )


class BackupFileFilterForm(BootstrapMixin, forms.Form):
    model = BackupFile
    q = forms.CharField(
        required=False,
        label='Search'
    )
    upload_server_id = forms.ModelChoiceField(
        queryset=UploadServer.objects.all(),
        required=False,
        to_field_name='id',
        label='Upload Server',
        widget=StaticSelect2()
    )
