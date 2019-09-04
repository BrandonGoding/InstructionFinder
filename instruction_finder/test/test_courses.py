""" Test Course """
from django.test import TestCase
from model_mommy import mommy
import mongoengine
from instruction_finder.models import Course


class TestCourse(TestCase):
    """
    Testing Course Model
    """

    def setUp(self):
        # Disconnect default settings connection
        mongoengine.connection.disconnect()

        # Connect with mongo mock for testing
        self.conn = mongoengine.connect("testdb", host="mongomock://localhost")

        self.course = mommy.make(Course, title="Tennis Lessons")


    def test_course_creation(self):
        # Test UserProfile Model creation
        self.assertTrue(isinstance(self.course, Course))


    def tearDown(self):
        # Drop test DB and close connection
        self.conn.drop_database("testdb")
        self.conn.close()
