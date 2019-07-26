from django.test import TestCase
from model_mommy import mommy
import mongoengine
import datetime
from instruction_finder.models import User, Profile, Course, Session, Seat
from instruction_finder.mongo_models import AvailableDay, SlotGroup, Slot


class TestUsers(TestCase):
    """
    Test User Model
    """

    def setUp(self):
        self.user = mommy.make(User,
                               email='user123@inst.com')

    def test_users_creation(self):
        self.assertTrue(isinstance(self.user, User))
        self.assertEqual(self.user.email, 'user123@inst.com')


class TestUserProfile(TestCase):
    """
    Test User Profile Model
    """

    def setUp(self):
        self.user = mommy.make(User,
                               email='user456@inst.com')

        self.user_profile = mommy.make(Profile,
                                       user=self.user,
                                       profile_type='student')

    def test_user_profile_creation(self):
        self.assertTrue(isinstance(self.user_profile, Profile))
        self.assertEqual(self.user_profile.profile_type, 'student')
        self.assertEqual(self.user_profile.user.email, 'user456@inst.com')


class TestCourseAndSessions(TestCase):
    """
    Test Course and Sessions Model
    """

    def setUp(self):
        # Disconnect default settings connection
        mongoengine.connection.disconnect()

        # Connect with mongomock for testing
        self.conn = mongoengine.connect('testdb', host='mongomock://localhost')

        self.instructor = mommy.make(User,
                                     email='instructor789@inst.com')
        self.instructor_profile = mommy.make(Profile,
                                             user=self.instructor,
                                             profile_type='instructor')

        self.course = mommy.make(Course,
                                 instructor=self.instructor,
                                 title='Tennis Lessons')

        # Create a session
        self.session = mommy.make(Session,
                                  course=self.course,
                                  date=datetime.datetime(2019, 8, 1),
                                  minutes_length=60,
                                  price=25.93)

        # Create 10 seats for 10 students in the section
        for i in range(1, 11):
            # Create some student
            student = mommy.make(User, email=f'student{i}@inst.com')
            mommy.make(Profile,
                       user=student,
                       profile_type='student')

            # Create a seat
            self.seat = mommy.make(Seat,
                       session=self.session,
                       student=student,
                       amount_paid=25.93,
                       status='confirmed')


        # Create 2 slot groups
        group_a = SlotGroup()
        group_a.group_name = 'Morning'

        group_b = SlotGroup()
        group_b.group_name = 'Night'

        # Create the slot hours inside the groups
        group_a.slots.append(Slot(hour='08:00'))
        group_a.slots.append(Slot(hour='08:30'))

        group_b.slots.append(Slot(hour='21:00'))
        group_b.slots.append(Slot(hour='21:30'))

        group_a.save()
        group_b.save()

        for i in range(1, 21):
            available_day = AvailableDay()
            available_day.day = datetime.datetime(2019, 8, i)
            available_day.instructor_id = self.instructor.id
            available_day.slot_group_ids.append(group_a.id)
            available_day.slot_group_ids.append(group_b.id)
            available_day.save()

    def tearDown(self):
        # Drop test DB and close connection
        self.conn.drop_database('testdb')
        self.conn.close()

    def test_course_creation(self):
        self.assertTrue(isinstance(self.course, Course))
        self.assertEqual(self.course.instructor.id, self.instructor.id)

    def test_session_creation(self):
        self.assertTrue(isinstance(self.session, Session))
        self.assertEqual(self.session.course_id, self.course.id)

        # Assert a session has been created
        self.assertEqual(Session.objects.count(), 1)

        # Assert that 10 seats has been created on the session
        self.assertEqual(self.session.seats.count(), 10)

        # Check relations from seat
        self.assertEqual(self.seat.session.course.instructor.email, 'instructor789@inst.com')
        self.assertEqual(self.seat.session.course.title, 'Tennis Lessons')

