import sys
import tensorflow as tf

__logger_version__ = "0.0.1"

def version():
    return __logger_version__

"""
    TIME LOGGER

    TIME MANAGER (HOSTS JOBS AND MANAGES DATA FOR JOBS)

    -> JOBS FIND DEFINED NEEDS FOR THE JOB AND OBTAIN THAT DATA IF POSSIBLE 
"""

class TimeManager():

    def __init__(self):
        self.stack = []

    def start_job(self, input):
        pass