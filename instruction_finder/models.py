from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from localflavor.us.models import USStateField

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
    To store additional user fields
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


class Course(models.Model):
    """
    Course Model
    """
    instructor = models.ForeignKey(User, on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Session(models.Model):
    """
    Session Model
    """
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name='sessions')
    minutes_length = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=12)
    currency = models.CharField(max_length=3, default='USD')

    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=45, null=True, blank=True)
    state = USStateField(null=True, blank=True)
    zip_code = models.CharField(max_length=5, null=True, blank=True)
    lat = DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    long = DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Seat(models.Model):
    """
    Seat Model
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('missed', 'Missed'),
        ('re-scheduled', 'Re-Scheduled'),
        ('canceled', 'Canceled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    )

    session = models.ForeignKey(
        Session, on_delete=models.PROTECT, related_name='seats')
    student = models.ForeignKey(
        User, on_delete=models.PROTECT, related_name='seats')
    amount_paid = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00)
    date_paid = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES, default='pending')

