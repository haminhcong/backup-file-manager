from django.conf import settings
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User


class BackupFileManagerAdminSite(AdminSite):
    """
    Custom admin site
    """
    site_header = 'Backup File Manager Administration'
    site_title = 'Backup File Manager'
    site_url = '/{}'.format(settings.BASE_PATH)


admin_site = BackupFileManagerAdminSite(name='admin')

# Register external models
admin_site.register(Group, GroupAdmin)
admin_site.register(User, UserAdmin)
