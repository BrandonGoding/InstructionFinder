"""
Authors:  Robert Marinho & Brandon Goding

This module declares the models for the instruction_finder APP.

Todo:
    * Review models.py and think of any methods that may be useful <-- Both of us
    * Review  https://docs.djangoproject.com/en/2.2/topics/i18n/translation/  <-- Brandon
    * Create class Student extends User        <-- Brandon Will DO
    * Create class Instructor extends User     <-- Brandon Will Do
    * Create class Administrator extends User  <-- Brandon Will Do
    * Create methods  for classes above        <-- Brandon Will Do Robert will review an test
    * Finish CourseAttribute class             <-- Robert Will Do
    * GOAT Test                                <-- Robert Will Do
    * COURSE RATING MODELS

"""
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from localflavor.us.models import USStateField
from mongoengine import *
from instruction_finder.helpers import RandomFileName
from instruction_finder.managers import UserManager
from instruction_finder.mongo_models import CourseAttributes


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User Model
    This is how we are going to customize fields in the default User Model
    """
    email = models.EmailField(
        _("email address"),
        unique=True,
        help_text=_(
            "Please enter a valid email address, this will also be your user name."),
    )
    first_name = models.CharField(
        _("first name"),
        max_length=30,
        blank=True,
        help_text=_("Please enter your given name."),
    )
    last_name = models.CharField(
        _("last name"),
        max_length=150,
        blank=True,
        help_text=_("Please enter your family name."),
    )
    date_joined = models.DateTimeField(
        _("date joined"),
        auto_now_add=True,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_trusty = models.BooleanField(
        _("trusty"),
        default=False,
        help_text=_("Designates whether the user has confirmed his account."),
    )

    # Object Manager
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        """
        Returns the users email address
        :return:
        String: self.email
        """
        return self.email

    class Meta:
        """
        Meta
        """
        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def full_name(self):
        """
        Returns the full name of the user
        :return:
        String: self.first_name self.last_name
        """
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def short_name(self):
        """
        Returns the short display name for the rider ie The First Name
        :return:
        String: Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        :param subject:
        :param message:
        :param from_email:
        :param kwargs:
        :return:
        int: number of successful messages (0 or 1)
        """
        # Sends an email to this User.
        send_mail(subject, message, from_email, [self.email], **kwargs)


class Profile(models.Model):
    """
    User Profile Model
    To store additional user fields
    """
    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE, related_name="user_profile"
    )
    avatar = models.ImageField(
        null=True, blank=True, upload_to=RandomFileName("user_profile")
    )
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        """
        Returns the email address of the profiles User
        :return:
        String: self.user
        """
        return f"Profile of {self.user}"

    @property
    def full_name(self):
        return self.user.full_name


class Instructor(Profile):
    title = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name="Instructor Title",
        help_text="Enter your professional title here, examples Coach, Professor, Master"
    )

    def __str__(self):
        """
        Returns the full name of the Instructor
        :return:
        String full_name
        """
        if self.title:
            return f"{self.title} {self.full_name}"
        return f"Instructor {self.full_name}"

    @property
    def average_rating(self):
        """
        Return the average rating calculated by total review score / count of reviews
        :return:
        int:
        """
        # TODO: FINISH THIS METHOD
        pass

    @property
    def courses_taught(self):
        """
        Returns the total number of courses taught on this app
        :return:
        int:
        """
        pass  # TODO: FINISH THIS METHOD

    def get_upcoming_courses(self):
        """
        Returns a list of upcoming class objects
        :return:
        List:
        """
        return Course.objects.filter(
            user=self.user.pk)  # TODO: NEED TO ALSO FILTER BY DATE


class Student(Profile):

    def __str__(self):
        """
        Returns the full name of the Student
        :return:
        String full_name
        """
        return f"Student {self.full_name}"


class Course(models.Model):
    """
    Course Model
    """
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.PROTECT,
        verbose_name=_("Course Instructor"),
        related_name="courses",
        null=False,
        blank=False,
    )
    title = models.CharField(
        max_length=200, verbose_name=_("Course Title"), null=False, blank=False
    )
    description = models.TextField(
        verbose_name=_("Course Description"), null=False, blank=False
    )

    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # PK to the CourseAttributes Document
    course_attributes_id = models.CharField(max_length=100, unique=True, default=None, null=True, blank=True)

    def __str__(self):
        """
        Returns the title of the course
        :return:
        String: title
        """
        return self.title

    def create_course_attributes_object(self):
        """
        Create course attributes in mongo DB (Will be used in the query)
        :return: None
        """
        course_attributes = CourseAttributes()
        course_attributes.course_id = self.pk
        course_attributes.course_title = self.title
        course_attributes.course_description = self.description
        course_attributes.is_active = self.is_active
        course_attributes.save()
        return course_attributes


    def get_course_attributes_object(self):
        """
        Return the course_attributes object
        :return: CourseAttributes()
        """
        try:
            return CourseAttributes.objects.get(id=self.course_attributes_id)
        except KeyError:
            raise KeyError('Attribute object not found')

        return None

    @property
    def upcoming(self):
        """
        Returns True if course has availability in upcoming session dates.
        :return:
        bool
        """
        pass


class Session(models.Model):
    """
    Session Model
    """

    course = models.ForeignKey(
        Course,
        on_delete=models.PROTECT,
        related_name="sessions",
        verbose_name=_("Course Session"),
    )
    minutes_length = models.IntegerField(verbose_name=_("Session Length"))
    price = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        null=False,
        blank=False,
        verbose_name=_("Session Price"),
    )
    currency = models.CharField(max_length=3, default="USD", verbose_name=_("Currency"))
    address = models.CharField(
        max_length=200, null=True, blank=True, verbose_name=_("Address")
    )
    city = models.CharField(
        max_length=45, null=True, blank=True, verbose_name=_("City")
    )
    state = USStateField(null=True, blank=True, verbose_name=_("State"))
    zip_code = models.CharField(
        max_length=5, null=True, blank=True, verbose_name=_("Postal Code")
    )
    lat = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name=_("Latitude"),
    )
    long = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        null=True,
        blank=True,
        verbose_name=_("Longitude"),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Seat(models.Model):
    """
    Seat Model
    """

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("missed", "Missed"),
        ("re-scheduled", "Re-Scheduled"),
        ("canceled", "Canceled"),
        ("confirmed", "Confirmed"),
        ("completed", "Completed"),
    )

    session = models.ForeignKey(
        Session,
        on_delete=models.PROTECT,
        related_name="seats",
        verbose_name=_("Seat Session"),
    )
    student = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="seats",
        verbose_name=_("Seat Student"),
    )
    amount_paid = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.00, verbose_name=_("Ammount Paid")
    )
    date_paid = models.DateTimeField(
        blank=True, null=True, verbose_name=_("Payment Made Date")
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending",
        verbose_name=_("Status"),
    )


@receiver(models.signals.post_save, sender=Course)
def create_course_attributes_object(sender, instance, **kwargs):

    """
    After a course is saved we create the course attributes
    in Mongo automatically
    """
    course_attributes = instance.create_course_attributes_object()
    instance.course_attributes_id = course_attributes.id

