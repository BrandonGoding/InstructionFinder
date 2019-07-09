import datetime
import mongoengine
from instructionApp.settings import MONGODB_NAME, MONGODB_USER,MONGODB_PWD

mongoengine.connect(MONGODB_NAME,
                    username=MONGODB_USER,
                    password=MONGODB_PWD,
                    authentication_source='admin')

# All models in this file are handled by Mongo

class Course(mongoengine.Document):
    title = mongoengine.StringField(required=True)
    description = mongoengine.StringField(required=True)
    instructor_id = mongoengine.IntField(required=True)
    is_active = mongoengine.BooleanField(required=True, default=True)
    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)

    meta = {
        'collection': 'courses'
    }