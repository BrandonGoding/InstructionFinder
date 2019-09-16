import datetime
import mongoengine


# All models in this file are handled by Mongo

class Tag(mongoengine.EmbeddedDocument):
    tag = mongoengine.StringField(required=True)


class CourseAttributes(mongoengine.Document):
    """
    Course Attributes will be used to store all attributes and tags of a Course
    Also it will be used in the Courses Finder Page
    In order to perform a serach operation

    e.g.
    {
        course_id: 100,             # PK in postgree
        course_title: "Night Tennis Classes"
        course_description: "Night Tennis Classes Description..."
        tags : [
                "tennis",
                "beginners",
                "night",
                "maine"
               ],
    }

    """

    course_id = mongoengine.IntField()
    course_title = mongoengine.StringField(required=True)
    is_active = mongoengine.BooleanField(required=True, default=False)
    course_description = mongoengine.StringField(required=True)
    tags = mongoengine.EmbeddedDocumentListField(Tag)
    custom = mongoengine.ListField()
