import datetime
import mongoengine
from instructionApp.settings import MONGODB_NAME, MONGODB_USER,MONGODB_PWD


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
        self.modified_date = datetime.datetime.now()
        return super(Session, self).save(*args, **kwargs)