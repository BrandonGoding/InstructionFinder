import datetime
import mongoengine

# All models in this file are handled by Mongo


class Seat(mongoengine.EmbeddedDocument):
    student_id = mongoengine.IntField(required=True)
    student_name = mongoengine.StringField()
    amount_paid = mongoengine.FloatField()
    date_paid = mongoengine.DateTimeField(default=datetime.datetime.now)


class Session(mongoengine.Document):
    course_id = mongoengine.IntField(required=True)
    course_title = mongoengine.StringField()
    instructor_id = mongoengine.IntField(required=True)
    instructor_name = mongoengine.StringField()
    session_date = mongoengine.DateTimeField()
    session_minutes_length = mongoengine.IntField(required=True)
    session_price = mongoengine.FloatField()
    session_currency = mongoengine.StringField(required=True)
    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated_at = mongoengine.DateTimeField(default=datetime.datetime.now)

    seats = mongoengine.EmbeddedDocumentListField(Seat)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Session, self).save(*args, **kwargs)

class Slot(mongoengine.EmbeddedDocument):
    """
    Slots Model
    This model is responsible to register the available slots of every half hour
    that the instructor would be available in a day

    e.g.

    '08:00',
    '08:30',
    '09:00',
    '09:30',
    '20:00',
    '20:30',
    '21:00',
    '21:30',

    """

    hour = mongoengine.StringField(required=True, unique=True)
    is_active = mongoengine.BooleanField(required=True,default=False)

class SlotGroup(mongoengine.Document):

    """
    The Instructor Can create different Slot Groups

    Let's suppose that the instructor Matt want to offer
    sessions on Sunday in the morning and on Friday at night...
    So he can create 2 different groups of available slots
    (One to specify slots of hour at night and other in the morning)

    """
    group_name = mongoengine.StringField()
    slots = mongoengine.EmbeddedDocumentListField(Slot)

class AvailableDay(mongoengine.Document):

    """
    The Instructor should be able to specify the available day
    Also a day can have one or more available slot groups
    """
    instructor_id = mongoengine.IntField(required=True)
    day = mongoengine.DateField(required=True)
    slot_group_ids = mongoengine.ListField()