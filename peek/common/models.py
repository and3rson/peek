from django.db import models
import uuid


class UUIDPrimaryKeyMixin(models.Model):
    class Meta:
        abstract = True

    id = models.UUIDField(primary_key=True, default=uuid.uuid1, editable=False)
