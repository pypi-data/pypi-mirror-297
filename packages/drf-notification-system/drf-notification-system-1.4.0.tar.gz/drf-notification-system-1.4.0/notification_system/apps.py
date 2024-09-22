from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class NotificationSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'notification_system'
    verbose_name = _("Notification System")
