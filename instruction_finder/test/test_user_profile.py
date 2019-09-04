"""Test User Profile """
from django.test import TestCase
from model_mommy import mommy

from instruction_finder.models import User, Profile


class TestUserProfile(TestCase):
    """
    Testing User Profile Model
    """

    def setUp(self):
        self.user = mommy.make(User, email="user456@inst.com")

        self.user_profile = mommy.make(Profile, user=self.user, profile_type="student")

    def test_user_profile_creation(self):
        # Test UserProfile Model creation

        self.assertTrue(isinstance(self.user_profile, Profile))
        self.assertEqual(self.user_profile.profile_type, "student")
        self.assertEqual(self.user_profile.user.email, "user456@inst.com")
