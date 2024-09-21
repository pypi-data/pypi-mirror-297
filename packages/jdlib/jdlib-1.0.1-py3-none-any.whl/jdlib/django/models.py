from django.db import models
from django.utils.translation import gettext_lazy as _

from jdlib.django.fields import AutoCreatedField, AutoLastModifiedField, UUIDField


class TimeStampedMixin(models.Model):
    created_at = AutoCreatedField()
    updated_at = AutoLastModifiedField()

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    uuid = UUIDField(_('UUID'))

    class Meta:
        abstract = True


class UUIDModel(TimeStampedMixin, UUIDMixin):
    class Meta:
        abstract = True
