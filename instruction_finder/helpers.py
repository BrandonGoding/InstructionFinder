import os
import uuid
from django.utils.deconstruct import deconstructible
from datetime import date

@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        # @note It's up to the validators to check if it's the correct file type in name or if one even exist.
        extension = os.path.splitext(filename)[1]
        return self.path % (uuid.uuid4(), extension)

class CustomCalculations():

    @staticmethod
    def calculate_age(date_of_birth):
        today = date.today()
        age = today.year - birthDate.year - (today.month, today.day) < (birthDate.month, birthDate.day)
        return age
