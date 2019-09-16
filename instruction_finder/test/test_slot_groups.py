""" Test Slot Groups """
from django.test import TestCase
from django.utils.timezone import utc
from model_mommy import mommy
from instruction_finder.models import Course, User, Instructor, Session, SlotGroup, \
    SessionSlot
import datetime


class TestSlotGroups(TestCase):
    """
    Testing Slot Groups
    """

    def setUp(self):
        # Instructor
        self.user = mommy.make(
            User, email="jacob@example.com", first_name="Jacob", last_name="Lee"
        )
        self.instructor = mommy.make(Instructor, user=self.user, title="Professor")

        # Course
        self.course = mommy.make(
            Course, instructor=self.instructor, title="Tennis Lessons"
        )

        # Session
        self.session = mommy.make(
            Session, course=self.course, price=23.34
        )

    def test_create_session_slot_groups(self):
        """create session slot group """

        # Create slots
        slot_morning = mommy.make(
            SlotGroup, name="Morning", instructor=self.instructor
        )
        slot_night = mommy.make(
            SlotGroup, name="Night", instructor=self.instructor
        )

        self.assertEqual(SlotGroup.objects.filter(instructor=self.instructor).count(),
                         2)

        # Add slot hours to the session
        slot_a = SessionSlot.objects.create(
            start=datetime.datetime(2920, 7, 1, 8, 0, 0, tzinfo=utc),
            end=datetime.datetime(2020, 7, 1, 9, 0, 0, tzinfo=utc),
            session=self.session,
            slot_group=slot_morning)

        slot_b = SessionSlot.objects.create(
            start=datetime.datetime(2920, 7, 1, 10, 0, 0, tzinfo=utc),
            end=datetime.datetime(2920, 7, 1, 11, 0, 0, tzinfo=utc),
            session=self.session,
            slot_group=slot_morning)

        slot_c = SessionSlot.objects.create(
            start=datetime.datetime(2920, 7, 1, 19, 0, 0, tzinfo=utc),
            end=datetime.datetime(2920, 7, 1, 20, 0, 0, tzinfo=utc),
            session=self.session,
            slot_group=slot_night)

        slot_d = SessionSlot.objects.create(
            start=datetime.datetime(1999, 7, 1, 21, 0, 0, tzinfo=utc),
            end=datetime.datetime(1999, 7, 1, 22, 0, 0, tzinfo=utc),
            session=self.session,
            slot_group=slot_night)


        self.assertEqual(self.session.session_slots.count(), 4)
