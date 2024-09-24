from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from jdlib.django.fields import AutoCreatedField, AutoUpdatedField, UUIDField


class SlugMixin(models.Model):
    slug = models.SlugField()

    SLUG_FIELD = 'name'

    class Meta:
        abstract = True

    def slugify(self):
        return slugify(getattr(self, self.SLUG_FIELD))
    
    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = self.slugify()
        super().save(*args, **kwargs)


class TimeStampedMixin(models.Model):
    created_at = AutoCreatedField()
    updated_at = AutoUpdatedField()

    class Meta:
        abstract = True


class UUIDMixin(models.Model):
    uuid = UUIDField(_('UUID'))

    class Meta:
        abstract = True


class SlugModel(SlugMixin, TimeStampedMixin):
    name = models.CharField(max_length=255)

    class Meta:
        abstract = True


class UUIDModel(TimeStampedMixin, UUIDMixin):
    class Meta:
        abstract = True


class User(AbstractUser, UUIDMixin):
    class Meta:
        abstract = True


class EmailUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if email is None:
            raise ValueError('Users must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)


class EmailUser(User):
    email = models.EmailField(_('email address'), unique=True)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = EmailUserManager()

    class Meta:
        abstract = True

    def __str__(self):
        return self.email
