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
from Utilities_jmorga24.properties import Property
from Utilities_jmorga24.property_plugins import UtcDate, MaxLenStr, IsDateOrDatetime, RequiredInt, RequiredString
from Utilities_jmorga24.log import get_logger
import db

log = get_logger("event")

class Keyed():
    # pylint: disable=too-few-public-methods
    '''
    A base class that ensures an imutable unique(ish) key for an instance.
    '''
    jm_key = Property(readonly=True)
    def __init__(self):
        self.__jm_key = str(uuid7())
        log.debug("This is the __init__ in Keyed: jm_key: %s", self.__jm_key)

# Application Classes
class Audited():
    # pylint: disable=too-few-public-methods
    ''' Generate audit values on a new instance
    '''
    creation_date = Property(readonly=True)
    def __init__(self):
        self.__creation_date = datetime.now().astimezone(ZoneInfo('UTC'))
        log.debug("This is the __init__ in Audited: creation_date = %s", self.__creation_date)


class Event(Keyed, Audited):
    # pylint: disable=too-few-public-methods
    '''
    A class that represents a single item in a calendar.
    '''
    start = Property(normalize=UtcDate, validate=IsDateOrDatetime)
    length = Property(validate=RequiredInt, data={"min_value": 0})
    title = Property(normalize=MaxLenStr, validate=RequiredString, data={"max_len": 25})
    description = Property()

    def __init__(self, *, title: str, evt_start: date | datetime,
                 evt_length_minutes: int = 0, description: str = ""):
        Keyed.__init__(self)
        Audited.__init__(self)
        self.start = evt_start
        self.length = evt_length_minutes
        self.title = title
        self.description = description if isinstance(
            description, str) and len(description) > 0 else self.title
        log.info("Created event: id=%s, title=%s", self.jm_key, self.title)

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
