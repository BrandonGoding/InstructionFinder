"""Test Users """
from django.test import TestCase
from model_mommy import mommy

from instruction_finder.models import User


class TestUsers(TestCase):
    """
    Testing User Class
    """

    def setUp(self):
        self.user = mommy.make(User, email="user123@inst.com")

    def test_users_creation(self):
        """
        Testing if the user is created corectly
        """
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.email, "user123@inst.com")
