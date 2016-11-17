from django.conf import settings
from django.db import models
from django.utils.timezone import now
from peek.common.models import UUIDPrimaryKeyMixin


class Note(UUIDPrimaryKeyMixin, models.Model):
    # class Meta:
    #     unique_together = (('owner', 'order'),)

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, blank=False)
    body = models.TextField()
    order = models.PositiveIntegerField(null=False, blank=False)
    color = models.CharField(max_length=6, default='FFFFFF', null=False, blank=False)
    created = models.DateTimeField(default=now)
    updated = models.DateTimeField(default=now)
