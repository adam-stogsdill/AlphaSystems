import json

from click import File
from datetime import datetime
from DatabaseIO import DatabaseHandler


class DatasetManager():

    def __init__(self, dataset_id: str, folder_location: str):
        """
        
        The DatasetManager class handles the dataset information. Essentially,
        this class will help manage the json information corresponding to 
        a certain dataset and its id.

        Args:
            dataset_id (str): The ID of the dataset within the database download
            folder_location (str): The folder location with the json data that you would like to load
                This should include all of the dataset IDs.
        """
        self.dataset_id = dataset_id
        self.dataset_location = folder_location
        self.metadata = {"dataset_changes":{}, "manual_metadata_changes":{}}
        
    def load_from_json(self, metadata_location: str):
        """ Load the metadata information from a given file location.

        Args:
            metadata_location (str): File location of the metadata json information.
        """
        with open(metadata_location) as file:
            self.metadata = json.load(file)[self.dataset_id]
            
    def load_from_azure_database(self, databaseHandler: DatabaseHandler):
        """[summary]

        Args:
            databaseHandler (DatabaseHandler): [description]
        """
        pass
    
    def get_metadata(self):
        return self.metadata

    def set_metadata(self, metadata: File):
        self.metadata = json.load(metadata)[self.dataset_id]

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
        self.metadata = {"file_changes":{}, "manual_metadata_changes":{}}
        
    def load_from_json(self, metadata_location: str):
        with open(metadata_location) as file:
            self.metadata = json.load(file)
            
    def load_from_azure_database(self, databaseHandler: DatabaseHandler):
        pass
    
    def get_metadata(self):
        return self.metadata

    def set_metadata(self, metadata: File):
        self.metadata = json.load(metadata)

    def append_process(self, process: str):
        utc_time = datetime.utcnow()
        self.metadata["file_changes"][str(utc_time)] = process
        self.metadata["manual_metadata_changes"] = ("append_process", process, str(utc_time))
        
    def delete_process(self, process: str):
        if len(self.metadata.keys()) == 0:
            raise Exception("METADATA LACKS INFORMATION")
        for timestamp in self.metadata:
            if self.metadata["dataset_changes"][timestamp] == process:
                utc_time = datetime.utcnow()
                self.metadata["manual_metadata_changes"] = ('delete_process', process, str(utc_time))