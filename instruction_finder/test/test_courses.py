""" Test Course """
import datetime

from django.test import TestCase
from django.utils.timezone import utc
from model_mommy import mommy
import mongoengine

from instructionApp.settings import MONGODB_PORT
from instruction_finder.models import Course, User, Instructor, SlotGroup, SessionSlot, \
    Session
from instruction_finder.mongo_models import CourseAttributes


class TestCourse(TestCase):
    """
    Testing Course Model
    """

    def setUp(self):
        # Disconnect default settings connection
        mongoengine.connection.disconnect()

        # Connect with mongo mock for testing
        self.conn = mongoengine.connect("testdb", host="mongomock://localhost",
                                        port=MONGODB_PORT)

        # Instructor
        self.user = mommy.make(
            User, email="jacob@example.com", first_name="Jacob", last_name="Lee"
        )
        self.instructor = mommy.make(Instructor, user=self.user, title="Professor")

        # Course
        self.course = mommy.make(
            Course, instructor=self.instructor, title="Tennis Lessons"
        )

    def test_course_creation(self):
        # Test UserProfile Model creation
        self.assertTrue(isinstance(self.course, Course))

    def test_is_active(self):
        self.assertFalse(self.course.is_active)

    def test_get_course_attributes_object(self):
        attrs = self.course.get_course_attributes_object()

        self.assertTrue(isinstance(attrs, CourseAttributes))
        self.assertEqual(attrs.course_id, self.course.id)
        self.assertEqual(attrs.course_title, "Tennis Lessons")

    def test_upcoming_events_with_open_slots(self):
        self.assertEqual(self.course.open_sessions.count(), 0)

        # Create a Session To the course
        self.session = mommy.make(
            Session, course=self.course, price=23.34
        )

        # Create slot
        slot_morning = mommy.make(
            SlotGroup, name="Morning", instructor=self.instructor
        )

        # Create some dates
        two_days_ago = datetime.datetime.today() - datetime.timedelta(days=2)
        two_days_ago = datetime.datetime(
            two_days_ago.year, two_days_ago.month, two_days_ago.day, 0, 0, 0, tzinfo=utc
        )

        yesterday = datetime.datetime.today() - datetime.timedelta(days=1)
        yesterday = datetime.datetime(
            yesterday.year, yesterday.month, yesterday.day, 0, 0, 0, tzinfo=utc
        )

        tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
        tomorrow = datetime.datetime(
            tomorrow.year, tomorrow.month, tomorrow.day, 0, 0, 0, tzinfo=utc
        )

        # Create a slot in the past
        past_slot = SessionSlot.objects.create(
            start=two_days_ago,
            end=yesterday,
            session=self.session,
            slot_group=slot_morning)

        # Remains with zero
        self.assertEqual(self.course.open_sessions.count(), 0)

        # Create a slot in the future
        future_slot = SessionSlot.objects.create(
            start=two_days_ago,
            end=tomorrow,
            session=self.session,
            slot_group=slot_morning)

        future_slot = SessionSlot.objects.create(
            start=yesterday,
            end=tomorrow,
            session=self.session,
            slot_group=slot_morning)


        self.assertEqual(self.course.open_sessions.count(), 2)


    def tearDown(self):
        # Drop test DB and close connection
        self.conn.drop_database("testdb")
        self.conn.close()
