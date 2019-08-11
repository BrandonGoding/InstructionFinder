import datetime
import mongoengine

# All models in this file are handled by Mongo


class Slot(mongoengine.EmbeddedDocument):

    """
    Start and End of the available slots
    """

    start = mongoengine.DateTimeField(required=True)
    end = mongoengine.DateTimeField(required=True)
    is_active = mongoengine.BooleanField(required=True, default=False)


class SlotGroup(mongoengine.Document):

    """
    The Instructor can create different available slot groups ('Morning', 'Evening')
    A slot group can have one or many slots of hour

    e.g

    {
        session_id: 14,
        group_name: 'Morning',
        slots: [
          {
            start: '2019-09-07T10:00:00.883Z',
            end: '2019-09-07T11:00:00.883Z',
            is_active: true
          },
          {
            start: '2019-09-07T11:00:00.883Z',
            end: '2019-09-07T12:00:00.883Z',
            is_active: false
          },
        ],
        created_at: '2019-08-07T02:47:57.883Z',
        updated_at: '2019-08-07T02:47:57.883Z',
    }
    """
    session_id = mongoengine.IntField(required=True)
    group_name = mongoengine.StringField(required=True)
    slots = mongoengine.EmbeddedDocumentListField(Slot)
    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated_at = mongoengine.DateTimeField(default=datetime.datetime.now)


class Tag(mongoengine.EmbeddedDocument):
    tag = mongoengine.StringField(required=True)


class CourseTags(mongoengine.Document):
    """
    Course Tags will be used in the Courses Finder Page
    In order to perform a tag query operation

    e.g.
    {
        course_id: 100,
        tags : [
                "tennis",
                "beginners",
                "night",
                "maine"
               ],
    }

    """
    course_id = mongoengine.IntField(required=True)
    tags = mongoengine.EmbeddedDocumentListField(Tag)
