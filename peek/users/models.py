from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from peek.common.models import UUIDPrimaryKeyMixin


class User(UUIDPrimaryKeyMixin, AbstractUser):
    class Meta:
        db_table = 'auth_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    photo = models.ImageField(_('Photo'), upload_to='users', blank=True)

    USERNAME_FIELD = 'username'
