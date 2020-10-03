from django.core.exceptions import ValidationError
from django.db import models

from extras.fields import IPAddressField
from extras.models import ChangeLoggedModel
from file_manager.constants import SERVER_TYPE_CHOICES, SERVER_TYPE_SYSTEM_SERVER, SERVER_TYPE_CLASSES


#
# Upload Server
#


class UploadServer(ChangeLoggedModel):
    """
    Represent upload server of file
    """
    name = models.CharField(
        max_length=50,
        unique=True
    )
    ip_address = IPAddressField(
        help_text='IPv4 or IPv6 address (with mask)',
        blank=True,
        null=True,
    )
    server_type = models.PositiveSmallIntegerField(
        choices=SERVER_TYPE_CHOICES
    )
    description = models.CharField(
        max_length=200,
        blank=True
    )
    slug = models.SlugField(
        unique=True
    )

    class Meta:
        ordering = ('name', 'slug')  # address may be non-unique
        verbose_name = 'Upload Server'
        verbose_name_plural = 'Upload Servers'

    def __str__(self):
        if self.ip_address:
            return f'{self.name} - {self.ip_address}'
        return self.name

    @property
    def server_ip_slug(self):
        return self.ip_address.ip.replace(':', '-').replace('.', '-')

    def get_duplicates(self):
        return UploadServer.objects.filter(
            address__net_host=str(self.ip_address.ip)).exclude(pk=self.pk)

    def clean(self):
        if self.server_type == SERVER_TYPE_SYSTEM_SERVER and not self.ip_address:
            raise ValidationError("Please specify server IP Address when upload server is system server")

        if self.ip_address:
            # /0 masks are not acceptable
            if self.ip_address.prefixlen == 0:
                raise ValidationError({
                    'address': "Cannot create IP address with /0 mask."
                })

            duplicate_ips = self.get_duplicates()
            if duplicate_ips:
                raise ValidationError({
                    'address': "Duplicate IP address {} with Server {}".format(
                        self.ip_address, duplicate_ips.first(),
                    )
                })

    def get_server_type_class(self):
        return SERVER_TYPE_CLASSES[self.server_type]


def backup_file_upload(instance, filename):
    backup_file_dir = 'backup-files'
    # Rename the file to the provided name
    storage_filename = (f'{instance.upload_server.server_ip_slug}-'
                        f'{instance.uuid}-f{instance.filename}')
    return '{}/{}'.format(backup_file_dir, storage_filename)


class BackupFile(ChangeLoggedModel):
    """
    An uploaded file which is associated with an object.
    """
    upload_server = models.ForeignKey(
        to=UploadServer,
        on_delete=models.PROTECT,
        related_name='backup_files'
    )
    absolute_file_path = models.CharField(
        blank=False,
        max_length=2048
    )
    filename = models.CharField(
        blank=False,
        max_length=256
    )
    uuid = models.UUIDField(
        editable=False
    )
    file = models.FileField(
        upload_to=backup_file_upload,
    )

    class Meta:
        ordering = ['upload_server', 'filename']
        unique_together = [
            ['upload_server', 'absolute_file_path'],
        ]

    def __str__(self):
        return f'{self.upload_server}-{self.filename}'

    def clean(self):
        if not self.absolute_file_path.endswith(self.filename):
            raise ValidationError("absolute file path is not contains file name")
