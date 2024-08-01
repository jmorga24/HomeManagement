'''
Class for the home management application.

Classes:
Keyed: A base class that ensures a unique(ish) key using a uuid.
Audited: A base class that ensures that we add the date created field to an instance
Event: Represents a single entry into a calendar.
Account: Represents a single account.

'''
from datetime import datetime, timedelta, date
from zoneinfo import ZoneInfo
from uuid_extensions import uuid7  # type: ignore
from properties import Property, ReadOnlyProperty
from property_plugins import UtcDate, MaxLenStr, IsDateOrDatetime, RequiredInt, RequiredString


class Keyed():
    # pylint: disable=too-few-public-methods
    '''
    A base class that ensures an imutable unique(ish) key for an instance.
    '''
    jm_key = ReadOnlyProperty(initial_value=str(uuid7()))

# Application Classes


class Audited():
    # pylint: disable=too-few-public-methods
    ''' Generate audit values on a new instance
    '''
    creation_date = ReadOnlyProperty(
        initial_value=datetime.now().astimezone(ZoneInfo('UTC')))


class Event(Keyed, Audited):
    # pylint: disable=too-few-public-methods
    '''
    A class that represents a single item in a calendar.
    '''
    start = Property(normalize=UtcDate, validate=IsDateOrDatetime)
    length = Property(validate=RequiredInt, data={"min_value": 0})
    title = Property(normalize=MaxLenStr,
                     validate=RequiredString, data={"max_len": 25})
    description = Property()

    def __init__(self, *, title: str, evt_start: date | datetime,
                 evt_length_minutes: int = 0, description: str = ""):
        super().__init__()
        self.start = evt_start
        self.length = evt_length_minutes
        self.title = title
        self.description = description if isinstance(
            description, str) and len(description) > 0 else self.title

    def end(self):
        ''' Calculate the end time of the event based on the start datetime 
        and a timedelta with the event's length.
        '''
        return self.start + timedelta(minutes=self.length)


# class Account(Keyed, Audited):

#     name = Property()
#     website = Property()
#     loginid = Property()
#     password = Property()
#     description = Property()
#     contact_name = Property()
#     contact_phone = Property()
