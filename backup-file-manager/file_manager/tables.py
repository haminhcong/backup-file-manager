import django_tables2 as tables

from file_manager.models import UploadServer, BackupFile
from utilities.tables import BaseTable

#
# Upload Server
#
SERVER_TYPE_LABEL = """
<span class="label label-{{ record.get_server_type_class }}">{{ record.get_server_type_display }}</span>
"""

BACKUP_FILE_SERVER = """
{{ record.upload_server.short_name }}
"""

BACKUP_FILE_SIZE = """
{% if record.file %}
    {{ record.size|filesizeformat }}
{% else %}
    &mdash;
{% endif %}
"""

BACKUP_FILE_DOWNLOAD_LINK = """
{% if record.file %}
    <a href="{{ record.file.url }}" target="_blank">{{ record.filename }}</a>
{% else %}
    &mdash;
{% endif %}
"""


class UploadServerTable(BaseTable):
    server_type = tables.TemplateColumn(SERVER_TYPE_LABEL, verbose_name='Server Type')

    class Meta(BaseTable.Meta):
        model = UploadServer
        fields = (
            'name', 'ip_address', 'server_type'
        )


class BackupFileTable(BaseTable):
    upload_server = tables.TemplateColumn(BACKUP_FILE_SERVER, verbose_name='Upload Server')
    file_size = tables.TemplateColumn(BACKUP_FILE_SIZE, verbose_name='Size')
    download_link = tables.TemplateColumn(BACKUP_FILE_DOWNLOAD_LINK, verbose_name='Download')

    class Meta(BaseTable.Meta):
        model = BackupFile
        fields = (
            'upload_server', 'absolute_file_path', 'filename', 'file_size', 'download_link'
        )
