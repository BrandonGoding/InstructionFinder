""" Test Course """
from django.test import TestCase
from model_mommy import mommy
import mongoengine
from instruction_finder.models import Course, User, Instructor
from instruction_finder.mongo_models import CourseAttributes


class TestCourse(TestCase):
    """
    Testing Course Model
    """

    def setUp(self):
        # Disconnect default settings connection
        mongoengine.connection.disconnect()

        # Connect with mongo mock for testing
        self.conn = mongoengine.connect("testdb", host="mongomock://localhost")


        # Instructor
        self.user = mommy.make(
            User, email="jacob@example.com", first_name="Jacob", last_name="Lee"
        )
        self.instructor = mommy.make(Instructor, user=self.user, title="Professor")


        # Course
        self.course = mommy.make(Course, instructor=self.instructor,
                                 title="Tennis Lessons")


    def test_course_creation(self):
        # Test UserProfile Model creation
        self.assertTrue(isinstance(self.course, Course))

    def test_is_active(self):
        self.assertFalse(self.course.is_active)

    def test_object_has_courseAttributes(self):
        self.assertIsNotNone(self.course.course_attributes_id)

    def test_get_course_attributes_object(self):
        attrs = self.course.get_course_attributes_object()

        self.assertTrue(isinstance(attrs, CourseAttributes))
        self.assertTrue(attrs.course_id, self.course.id)
        self.assertTrue(attrs.course_title, "Tennis Lessons")

        # Saving Custom Attributes
        attrs.custom = {"a": 213}
        attrs.save()

        self.assertTrue(self.course.get_course_attributes_object().custom["a"], "123")


    def tearDown(self):
        # Drop test DB and close connection
        self.conn.drop_database("testdb")
        self.conn.close()
