from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from instruction_finder.mongo_models import Session, Seat
import random
import datetime
from instruction_finder.models import Course, User, Profile


# Testing CREATE models
class TestCourseView(View):
    def get(self, request, *args, **kwargs):
        # Create Instructor
        rand = random.randint(0, 1000)
        instructor = User.objects.create_user(email=f'instructor{rand}@gmail.com',
                                              password='c9rj7g!!',
                                              first_name="Instructor",
                                              last_name=f"{rand}")
        Profile.objects.create(profile_type='instructor', user=instructor)

        # Create Student
        rand = random.randint(0, 1000)
        student = User.objects.create_user(email=f'student{rand}@gmail.com',
                                           password='c9rj7g!!',
                                           first_name="Student",
                                           last_name=f"{rand}")
        Profile.objects.create(profile_type='student', user=student)

        # Create a course on POSTGRES
        course = Course.objects.create(instructor=instructor,
                                       title='Tennis Lessons',
                                       description='This is the description of the course')

        # Create a session for the course in MONGO
        session = Session()
        session.course_id = course.id
        session.course_title = course.title
        session.instructor_id = instructor.id
        session.instructor_name = instructor.get_full_name() if instructor.get_full_name() else instructor.get_username()
        session.session_date = datetime.datetime(2019, 8, 1)
        session.session_minutes_length = 120
        session.session_price = 45.98
        session.session_currency = 'us-dollar'

        # Create seats
        seat = Seat()
        seat.student_id = student.id
        seat.student_name = student.get_full_name() if student.get_full_name() else student.get_username()
        seat.amount_paid = 45.98
        seat.date_paid = datetime.datetime(2019, 7, 1)

        # Link seat to the session seats
        session.seats.append(seat)
        session.save()

        return JsonResponse(
            {
                "ok": "test",
                "session": session.to_json()
            },
            status=200,
            safe=False)
