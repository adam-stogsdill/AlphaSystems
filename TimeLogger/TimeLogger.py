import sys
import tensorflow as tf
from datetime import datetime

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
        self.data = []
        pass

    def start(self, action: str):
        utc_time = datetime.utcnow()
        self.data.append(('start', utc_time, action))
        pass

    def end(self, action: str):
        utc_time = datetime.utcnow()
        self.data.append(('end',utc_time, action))
        pass



class TimeManager():

    def __init__(self):
        self.stack = {}

    def start_job(self, action: str):
        pass

