""" Test Session """
from django.test import TestCase
from model_mommy import mommy
from instruction_finder.models import Course, User, Instructor, Session


class TestSession(TestCase):
    """
    Testing Session Model
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

    def test_session_creation(self):
        # Test UserProfile Model creation

        session = mommy.make(
            Session, course=self.course, price=23.34
        )
        self.assertTrue(isinstance(session, Session))

        self.assertEqual(self.course.sessions.count(), 1)
