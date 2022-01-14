import sys
from tracemalloc import start
import tensorflow as tf
from datetime import datetime
from uuid import uuid4, UUID

__logger_version__ = "0.0.1"

def version():
    return __logger_version__

"""
    TIME LOGGER

    TIME MANAGER (HOSTS JOBS AND MANAGES DATA FOR JOBS)

    -> JOBS FIND DEFINED NEEDS FOR THE JOB AND OBTAIN THAT DATA IF POSSIBLE 
"""

class Job:
    
    def __init__(self):
        self.data = {}
        self.__serials__ = set() # Maintain a running knowledge of serials within this Job

    def start(self, serial: UUID):
        utc_time = datetime.utcnow()
        self.data['start_'+str(serial)] = utc_time
        self.__serials__.add(serial)
        return True

    def end(self, serial: UUID):
        utc_time = datetime.utcnow()
        self.data['end_'+str(serial)] = utc_time
        return True

    def is_complete(self):
        # Return True if there is a even set of start and end times
        for serial in self.__serials__:
            if 'start_'+str(serial) not in self.data and 'end_'+str(serial) not in self.data:
                return False
        return True


class TimeManager():

    def __init__(self, name: str):
        # Stack keys: (action)
        self.__stack__ = {}
        self.name = name

    # Start a timing job
    # Return a serial for ending a job
    def start_job(self, action: str):
        # Generate UUID
        serial = uuid4()
        
        if action not in self.stack:
            self.__stack__[action] = Job()
        self.__stack__[action].start(serial)
        return serial

    def end_job(self, action: str, serial: UUID):
        if action not in self.stack:
            raise Exception("JOB DID NOT PREVIOUSLY EXIST WITHIN THE TIME MANAGER CALLED:", self.name)
        self.__stack__[action].end(serial)


