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
    group_name = mongoengine.StringField()
    slots = mongoengine.EmbeddedDocumentListField(Slot)
    created_at = mongoengine.DateTimeField(default=datetime.datetime.now)
    updated_at = mongoengine.DateTimeField(default=datetime.datetime.now)
