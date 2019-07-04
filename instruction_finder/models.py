from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from djongo import models
from instruction_finder.managers import UserManager
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _
from instruction_finder.helpers import RandomFileName
from mongoengine import *


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    This is how we are going to customize fields in the default User Model
    """
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    is_trusty = models.BooleanField(
        _('trusty'),
        default=False,
        help_text=_(
            'Designates whether the user has confirmed his account.'
        )
    )

    # Object Manager
    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        # Returns the first_name plus the last_name, with a space in between.
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        # Returns the short name for the user.
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        # Sends an email to this User.
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(models.Model):
    """
    User Profile Model
    """
    PROFILE_TYPES = [
        ('student', 'Student'),
        ('instructor', 'Instructor'),
        ('admin', 'Administration'),
    ]

    profile_type = models.CharField(max_length=15, choices=PROFILE_TYPES)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='user_profile')
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=RandomFileName('user_profile')
    )
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user}"


class Session(models.Model):
    """
    Session Model
    """
    session_date_time = models.DateTimeField()
    session_length = models.IntegerField()
    session_price = models.DecimalField(
        decimal_places=2,
        max_digits=8,
        default='00.00')

    class Meta:
        abstract = True


class Course(models.Model):
    """
    Course Model
    """
    instructor = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.TextField()

    # Embedded Sessions
    sessions = models.EmbeddedModelField(model_container=Session)

    def __str__(self):
        return self.title
