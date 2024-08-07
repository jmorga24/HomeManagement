'''
Unit tests for jm_classes.Event class.
'''
import sys
from datetime import date, datetime, timedelta
from time import time
from zoneinfo import ZoneInfo

import pytest
from uuid_extensions import uuid7 # type: ignore

sys.path.append("..")
from jm_classes import Event
from Utilities_jmorga24.property_plugins import PluginError

class TestEventClass():
    '''
    Unit tests for jm_classes.Event class.
    '''
    def today_as_number(self):
        '''
        Get the date as a int - to test submitting a numeric.
        '''
        return datetime.now().year * 10000 + datetime.now().month*100 + datetime.now().day

    def test_create_instance_of_event(self):
        ''' Confirm that basic instantiation works
            1: We get an instance of Event
            2: The title property is correct
            3: The start property is an instance of datetime
            4: The length property is correct
            5: The description property is correct
            6: The end property is an instance of datetime
            7: The end property is correct based on the start property + the length property       
        '''
        t = datetime.now()
        e = Event(title="Test", evt_start=t, evt_length_minutes=60,
                  description="This is the long description")

        assert isinstance(e, Event)
        assert e.title == "Test"
        assert isinstance(e.start, datetime)
        assert e.start == t.astimezone(tz= ZoneInfo('UTC'))
        assert e.length == 60
        assert e.description == "This is the long description"
        assert isinstance(e.end(), datetime)
        assert e.end() == e.start + timedelta(minutes = 60)
        assert isinstance(e.creation_date, datetime)
        assert e.jm_key


    def test_create_instance_of_event_with_date(self):
        ''' Confirm that passing a date as the start argument works
            1: We get an instance of Event
            3: The start property is an instance of datetime
            4: The start property matches the input date
        '''
        t = datetime.now().date()
        e = Event(title="Test", evt_start= t, evt_length_minutes=60, description="This is the long description")
        assert isinstance(e, Event)
        assert isinstance(e.start, datetime)
        # we expect e.start to be midnight of the date input adjusted to UTC
        assert e.start == datetime(t.year, t.month, t.day, hour=0, minute=0, second=0).astimezone(tz=ZoneInfo('UTC'))


    def test_create_instance_with_long_title(self):
        ''' Confirm that passing a long title - currently title length is limited to 25 chars
            1: We get an instance of Event
            3: The title property is truncated  
        '''
        e = Event(title="TestxTestxTestxTestxTestxTestxTestxTestx",
                  evt_start= datetime.now(), evt_length_minutes=60,
                  description="This is the long description")
        assert isinstance(e, Event)
        assert len(e.title) == 25
        assert e.title[-3:] == "..."
        print(e.title)

    def test_create_instance_length_zero(self):
        ''' Confirm that passing a date as the start argument works
            1: We get an instance of Event
            3: The start time equals the end time    
        '''
        e = Event(title="Test", 
                  evt_start= datetime.now(), evt_length_minutes=0,
                  description="This is the long description")
        assert isinstance(e, Event)
        assert e.start == e.end()

    # **** Test failure to instantiate
    def test_create_with_invalid_date(self):
        # pylint: disable=missing-kwoa
        ''' Confirm that basic instantiation fails if we pass None as the start time 
        '''
        with pytest.raises(TypeError):
            _ = Event(title="Test", evt_length_minutes=60,
                      description="This is the long description")

    def test_create_with_string_for_date(self):
        ''' Confirm that basic instantiation fails if we pass a string as the start time 
        '''
        with pytest.raises(PluginError):
            _ = Event(title="Test",
                      evt_start= datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
                      evt_length_minutes=60, description="This is the long description")

    def test_create_with_numeric_for_date(self):
        ''' Confirm that basic instantiation fails if we pass an integer as the start time 
        '''
        with pytest.raises(PluginError):
            _ = Event(title="Test", evt_start= self.today_as_number(),
                      evt_length_minutes=60, description="This is the long description")

    def test_create_with_none_for_title(self):
        ''' Confirm that basic instantiation fails if we pass None as the title 
        '''
        with pytest.raises(PluginError):
            _ = Event(title=None, evt_start= datetime.now(),
                      evt_length_minutes=60, description="This is the long description")

    def test_create_with_empty_string_for_title(self):
        ''' Confirm that basic instantiation fails if we pass zero length string as the title 
        '''
        with pytest.raises(PluginError):
            _ = Event(title='', evt_start= datetime.now(),
                      evt_length_minutes=60, description="This is the long description")

    def test_create_with_length_negative(self):
        ''' Confirm that basic instantiation fails if we pass zero length string as the title 
        '''
        with pytest.raises(PluginError):
            _ = Event(title='Title', evt_start= datetime.now(),
                      evt_length_minutes=-60, description="This is the long description")

    def test_create_with_length_none(self):
        ''' Confirm that basic instantiation fails if we pass zero length string as the title 
        '''
        with pytest.raises(PluginError):
            _ = Event(title='Title', evt_start= datetime.now(),
                      evt_length_minutes=None, description="This is the long description")

    def test_try_change_creation_date(self):
        ''' Confirm that attempting to change the creation date fails 
        '''
        e = Event(title='Title', evt_start= datetime.now(),
                  evt_length_minutes=60, description="This is the long description")
        with pytest.raises(AttributeError):
            e.creation_date = datetime.now() + timedelta(hours=3)

    def test_try_change_key(self):
        ''' Confirm that attempting to change the key date fails 
        '''
        e = Event(title='Title', evt_start= datetime.now(), evt_length_minutes=60,
                  description="This is the long description")
        with pytest.raises(AttributeError):
            e.jm_key = str(uuid7())
