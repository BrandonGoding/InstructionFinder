"""Test User Profile """
from django.test import TestCase
from model_mommy import mommy

from instruction_finder.models import (
    User,
    Profile,
    Instructor,
    Student,
    InstructorRating,
)


class TestUserProfile(TestCase):
    """
    Testing User Profile Model
    """

    def setUp(self):
        self.user = mommy.make(User, email="user456@example.com")
        self.user_profile = mommy.make(Profile, user=self.user)

    def test_user_profile_creation(self):
        # Test UserProfile Model creation
        self.assertTrue(isinstance(self.user_profile, Profile))
        self.assertEqual(self.user_profile.user.email, "user456@example.com")


class TestInstructorProfile(TestCase):
    """
    Testing Instructor Model
    """

    def setUp(self):
        self.user1 = mommy.make(
            User, email="user1@example.com", first_name="Jacob", last_name="Lee"
        )
        self.user2 = mommy.make(
            User, email="user2@example.com", first_name="Mary", last_name="Lee"
        )

        self.instructor1 = mommy.make(Instructor, user=self.user1, title="Professor")
        self.instructor2 = mommy.make(Instructor, user=self.user2)

    def test_number_of_created_profiles(self):
        """
        Assert that 2 Profile objects can be counted
        after creating 2 Instructor Models
        """
        self.assertEqual(Profile.objects.count(), 2)

    def test_string_version_of_instance(self):
        """
        Test the __str__ method of Instructor Model
        """
        self.assertEqual(str(self.instructor1), "Professor Jacob Lee")
        self.assertEqual(str(self.instructor2), "Instructor Mary Lee")


class TestStudentProfile(TestCase):
    """
    Testing Student Model
    """

    def setUp(self):
        self.user1 = mommy.make(
            User, email="user1@example.com", first_name="Jaden", last_name="Abe"
        )
        self.user2 = mommy.make(
            User, email="user2@example.com", first_name="Grace", last_name="Abe"
        )

        self.student1 = mommy.make(Student, user=self.user1)
        self.student2 = mommy.make(Student, user=self.user2)

    def test_number_of_created_profiles(self):
        """
        Assert that 2 Profile objects can be counted
        after creating 2 Student Models
        """
        self.assertEqual(Profile.objects.count(), 2)

    def test_string_version_of_instance(self):
        """
        Test the __str__ method of Student Model
        """
        self.assertEqual(str(self.student1), "Student Jaden Abe")
        self.assertEqual(str(self.student2), "Student Grace Abe")


# gonna comment out for now
# class TestRatings(TestCase):
#
#     def setUp(self):
#         self.user1 = mommy.make(
#             User, email="user1@example.com", first_name="Jacob", last_name="Lee"
#         )
#
#         self.instructor1 = mommy.make(Instructor, user=self.user1, title="Professor")
#
#         self.user3 = mommy.make(
#             User, email="user11@example.com", first_name="Jaden", last_name="Abe"
#         )
#         self.user2 = mommy.make(
#             User, email="user2@example.com", first_name="Grace", last_name="Abe"
#         )
#
#         self.student1 = mommy.make(Student, user=self.user3)
#         self.student2 = mommy.make(Student, user=self.user2)
#
#         self.rating1 = mommy.make(InstructorRating, instructor=self.instructor1, student=self.student1, rating=4)
#         self.rating2 = mommy.make(InstructorRating, instructor=self.instructor1, student=self.student2, rating=8)
#
#     def test_average_rating(self):
#         self.assertEqual(self.instructor1.average_rating, 6)
