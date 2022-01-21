import json

from click import File
from datetime import datetime
from DatabaseIO import DatabaseHandler


class DatasetManager():

    def __init__(self, folder_location: str):
        self.dataset_location = folder_location
        self.metadata = {"dataset_changes":{}, "manual_metadata_changes":{}}
        
    def load_from_json(self, metadata_location: str):
        with open(metadata_location) as file:
            self.metadata = json.load(file)
            
    def load_from_azure_database(self, databaseHandler: DatabaseHandler):
        pass

    def set_metadata(self, metadata: File):
        self.metadata = json.load(metadata)

    def append_process(self, process: str):
        utc_time = datetime.utcnow()
        self.metadata["dataset_changes"][str(utc_time)] = process
        self.metadata["manual_metadata_changes"] = ("append_process", process, str(utc_time))
        
    def delete_process(self, process: str):
        if len(self.metadata.keys()) == 0:
            raise Exception("METADATA LACKS INFORMATION")
        for timestamp in self.metadata:
            if self.metadata["dataset_changes"][timestamp] == process:
                utc_time = datetime.utcnow()
                self.metadata["manual_metadata_changes"] = ('delete_process', process, str(utc_time))
            
            
def FileManager():
    
    def __init__(self, file_location: str):
        self.file_location = file_location
        self.metadata = {}