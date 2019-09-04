"""Test Users """
from django.test import TestCase
from model_mommy import mommy

from instruction_finder.models import User


class TestUsers(TestCase):
    """
    Testing User Class
    """

    def setUp(self):
        self.user = mommy.make(
            User, email="user123@inst.com", first_name="Robert", last_name="Junior"
        )

    def test_users_creation(self):
        """
        Testing the user creation
        """
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.email, "user123@inst.com")

    def test_full_name_method(self):
        """Testing full_name() User method"""
        user = User.objects.get(pk=self.user.pk)
        self.assertEqual(user.full_name, "Robert Junior")
