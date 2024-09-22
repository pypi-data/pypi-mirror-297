from django.urls import path
from rest_framework import routers

from notification_system.api.views import (NotificationEventViewSet, EmailTemplateViewSet, OutgoingMessageViewSet,
                                           OutgoingMessageNotificationAPIView, NotificationGroupViewSet,
                                           SmtpProviderViewSet, MedialViewSet, ContactViewSet, ContactGroupViewSet)

app_name = "notification_events"

router = routers.SimpleRouter()
router.register("notification-events", NotificationEventViewSet, basename="notification_events")
router.register("email-templates", EmailTemplateViewSet, basename="email_templates")
router.register("outgoing-messages", OutgoingMessageViewSet, basename="outgoing_messages")
router.register("contacts", ContactViewSet, basename="contacts")
router.register("contact-groups", ContactGroupViewSet, basename="contact_groups")
router.register("notification-groups", NotificationGroupViewSet, basename="notification_groups")
router.register("smtp-providers", SmtpProviderViewSet, basename="smtp_providers")
router.register("media", MedialViewSet, basename="media")

urlpatterns = router.urls

urlpatterns += [
    path("outgoing-message-webhook/", OutgoingMessageNotificationAPIView.as_view(), name="outgoing_message_webhook"),
]
