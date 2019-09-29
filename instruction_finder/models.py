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
import datetime
import statistics
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django.utils.timezone import utc
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from localflavor.us.models import USStateField
from mongoengine import *
from instruction_finder.helpers import RandomFileName, CustomCalculations
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
            "Please enter a valid email address, this will also be your user name."
        ),
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
    date_joined = models.DateTimeField(_("date joined"), auto_now_add=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
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

    def __str__(self: object) -> str:
        """
        Returns the users full Name
        :return:
        String: self.email
        """
        return str(self.full_name)

    class Meta:
        """
        Meta
        """

        verbose_name = _("user")
        verbose_name_plural = _("users")

    @property
    def full_name(self: object) -> str:
        """
        Returns the full name of the user
        :return:
        String: self.first_name self.last_name
        """
        return str(f"{self.first_name} {self.last_name}".strip())

    @property
    def short_name(self: object) -> str:
        """
        Returns the short display name for the rider ie The First Name
        :return:
        String: Returns the short name for the user.
        """
        return str(self.first_name)

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

    # The Profile file Model has a one to one relation with User
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        related_name="user_profile",
        verbose_name=_("Profile's User"),
        help_text=_("Please select this profiles user."),
    )
    # We upload an avatar image for display in profiles, and comments
    avatar = models.ImageField(
        null=True,
        blank=True,
        upload_to=RandomFileName("user_profile"),
        verbose_name=_("User's Avatar"),
        help_text=_("Please select a image to use as your Avatar"),
    )
    # Used for administrative purposes and in some calculations
    # Required to make sure user can use site
    date_of_birth = models.DateField(
        null=False,
        blank=False,
        verbose_name=_("User's Date of Birth"),
        help_text=_("Please enter your date of birth"),
    )

    def __str__(self: object) -> str:
        """
        Returns a display title for the user profile
        :return: str: Profile of {self.user}
        """
        return str(f"Profile of {self.user}")

    @property
    def full_name(self: object) -> str:
        """
        Returns the full name of the user
        :return: str: self.user.full_name
        """
        return str(self.user.full_name)

    @property
    def age(self: object) -> int:
        """
        Returns the users age for display as an integer
        :return: int: CustomCalculations.calculate_age(self.date_of_birth)
        """
        return int(CustomCalculations.calculate_age(self.date_of_birth))


class Instructor(Profile):
    """
    The Instructor Class Extends Profile with Instructor Specific Fields
    """

    title = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        verbose_name="Instructor Title",
        help_text="Enter your professional title here, examples Coach, Professor, Master",
    )

    def __str__(self: object) -> str:
        """
        Returns the full name of the Instructor
        :return:
        String full_name
        """
        if self.title:
            return str(f"{self.title} {self.full_name}")
        return str(f"Instructor {self.full_name}")

    @property
    def average_rating(self: object) -> int:
        """
        Returns the average rating for the instructor
        :return: int: round(statistics.mean(numbers), 0)
        """
        ratings = self.instructor_ratings.all()
        numbers = []
        for rating in ratings:
            numbers.append(rating.rating)
        return int(round(statistics.mean(numbers), 0))

    # @property
    # def courses_taught(self: object):
    #     """
    #     Returns the total number of courses taught on this app
    #     :return:
    #     int:
    #     """
    #     pass

    def get_upcoming_courses(self: object) -> list:
        """
        Returns a list of upcoming class objects
        :return:
        List:
        """
        return Course.objects.filter(user=self.user.pk)


class Student(Profile):
    def __str__(self: object) -> str:
        """
        Returns the full name of the Student
        :return:
        String full_name
        """
        return str(f"Student {self.full_name}")

    @property
    def courses_taken(self: object) -> int:
        """
        Returns a count of the students completed courses
        :return: int: self.seats.filter(status='completed').count()
        """
        return int(self.seats.filter(status="completed").count())

    def get_course_reviews(self: object) -> list:
        """
        Returns a list of the students course ratings
        :return: list: self.course_ratings
        """
        return self.course_ratings


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

    def __str__(self: object) -> str:
        """
        Returns the title of the course
        :return:
        String: title
        """
        return str(self.title)

    def get_course_attributes_object(self: object):
        """
        Return the course_attributes object
        :return: CourseAttributes()
        """
        try:
            return CourseAttributes.objects.get(course_id=self.pk)
        except (KeyError, ValidationError):
            raise KeyError("Attribute object not found")

    @property
    def open_sessions(self: object):
        """
        Return the open sessions in the course
        :return: Session
        """

        today = datetime.datetime.today()
        today = datetime.datetime(
            today.year, today.month, today.day, 0, 0, 0, tzinfo=utc
        )
        return self.sessions.filter(session_slots__end__gte=today)


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


class SlotGroup(models.Model):
    """
    Slot Group Model
    """
    name = models.CharField(
        max_length=200, verbose_name=_("Slot Group"), null=False, blank=False
    )
    description = models.TextField(
        verbose_name=_("Slot Group Description"), null=True, blank=True
    )
    instructor = models.ForeignKey(
        Instructor,
        on_delete=models.CASCADE,
        verbose_name=_("Slot Groups"),
        related_name="slot_groups",
    )


class SessionSlot(models.Model):
    start = models.DateTimeField(verbose_name=_("Slot Start Date"))
    end = models.DateTimeField(verbose_name=_("Slot End Date"))
    session = models.ForeignKey(
        Session,
        on_delete=models.CASCADE,
        related_name="session_slots",
        verbose_name=_("Session Slots"),
    )
    slot_group = models.ForeignKey(
        SlotGroup,
        on_delete=models.CASCADE,
        related_name="session_slots",
        verbose_name=_("Session Slots"),
    )
    is_active = models.BooleanField(
        _("active"),
        default=False,
    )


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


class InstructorRating(models.Model):
    instructor = models.ForeignKey(
        to=Instructor,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="instructor_ratings",
    )
    student = models.ForeignKey(
        to=Student,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="instructor_ratings",
    )
    seat = models.ForeignKey(
        to=Seat,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="instructor_ratings",
    )
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    narrative = models.TextField(null=True, blank=True)

    def __meta__(self: object):
        unique_together = ("instructor", "student", "seat")

    @staticmethod
    def get_average_rating_by_instructor(instructor):
        ratings = InstructorRating.objects.filter(instructor=instructor)
        numbers = []
        for rating in ratings:
            numbers.append(rating.rating)
        return statistics.mean(numbers)


class CourseRating(models.Model):
    student = models.ForeignKey(
        to=Student,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="course_ratings",
    )
    course = models.ForeignKey(
        to=Course,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="course_ratings",
    )
    seat = models.ForeignKey(
        to=Seat,
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name="course_ratings",
    )
    rating = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    narrative = models.TextField(null=True, blank=True)

    def __meta__(self: object):
        unique_together = ("student", "course", "seat")

    @staticmethod
    def get_average_rating_by_course(course):
        """
        :param course:
        :return:
        """
        ratings = CourseRating.objects.filter(course=course)
        numbers = []
        for rating in ratings:
            numbers.append(rating.rating)
        return statistics.mean(numbers)


@receiver(models.signals.post_save, sender=Course)
def create_course_attributes_object(sender, instance, **kwargs):
    """
    After a course is saved CourseAttributes is created
    in Mongo
    """

    if CourseAttributes.objects.filter(course_id=instance.pk).count() > 0:
        CourseAttributes.objects.get(course_id=instance.pk).update(
            course_title=instance.title,
            course_description=instance.description,
            is_active=instance.is_active,
        )

    attributes = CourseAttributes()
    attributes.course_title = instance.title
    attributes.course_description = instance.description
    attributes.is_active = instance.is_active
    attributes.course_id = instance.pk
    attributes.save()
