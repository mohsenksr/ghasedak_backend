from enum import Enum

from django.contrib.auth.models import AbstractUser, Group, Permission, UserManager
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext as _
from simple_history.models import HistoricalRecords

from ghasedak.constants import PHONE_REGEX_PATTERN


class UserRoles(models.TextChoices):
    customer = 'CUSTOMER', _('customer')
    admin = 'ADMIN', _('admin')


def validate_user_role(value):
    if value not in UserRoles.values:
        raise ValidationError(_('user role is not valid'))


class CustomUserManager(UserManager):
    def create_user(self, username, email=None, password=None, **extra_fields):
        user = super().create_user(username, email, password, **extra_fields)
        return user


class User(AbstractUser):
    first_name = models.CharField(max_length=64, null=False, blank=False)
    last_name = models.CharField(max_length=64, null=False, blank=False)
    phone = models.CharField(
        validators=[RegexValidator(regex=PHONE_REGEX_PATTERN)],
        max_length=16,
        null=False,
        blank=False,
        unique=True
    )
    email = models.EmailField(null=True, blank=True, unique=True)
    cc_number = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )
    is_staff = models.BooleanField(
        default=False,
        help_text=_("designates whether the user can log into this admin site."),
    )
    national_id = models.CharField(max_length=20, null=True, blank=True)
    is_active = models.BooleanField(
        default=True,
        help_text=_(
            "designates whether this user should be treated as active. " "unselect this instead of deleting accounts."
        ),
    )
    role = models.CharField(max_length=32, choices=UserRoles.choices, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    modified_date = models.DateTimeField(auto_now=True, null=False, blank=False)
    credit = models.PositiveBigIntegerField(default=0, null=False, blank=False)
    groups = models.ManyToManyField(
        Group,
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="users",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="users",
        related_query_name="user",
    )
    history = HistoricalRecords()
    objects = CustomUserManager()

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name


class LoginTypes(Enum):
    PHONE = 0
    PASSWORD = 1
