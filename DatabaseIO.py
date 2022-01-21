import os
import pyodbc
import json
from azure.storage.blob import BlobServiceClient, ContainerClient, __version__
from azure.storage.blob.aio import BlobClient

__container_name__ = None
__connection_str__ = None

class DatabaseHandler:
    
    def __init__(self, json_file_location: str):
        self.conn = None
        self.cursor = None
        self.connect(json_file_location=json_file_location)
    
    def connect(self, json_file_location: str):
        '''
        connect to the db, open a buffered cursor
        
        Returns
        -------
        bool
            Tells user if funtion connected to DB successfully
        '''

        
        api_information = json.load(json_file_location)

        server = api_information['server']
        database = api_information['database']
        username = api_information['username']
        password = api_information['password']
        driver= api_information['driver']
        port = api_information['port']
        connstr = 'DRIVER='+driver+';SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+ password

        try:
            conn = pyodbc.connect(connstr)
            cursor = conn.cursor()
            return True

        except Error as e:
            print(e)
            return False
        
    def close(self):
        '''
        Closes DB connection
        
        Returns
        -------
        None.
        '''
        
        self.conn.close()
        
    def download(self, blob_url: str, download_file_location: str, download_file_name: str):
        try:
            blob_service_client = BlobServiceClient.from_connection_string(__connection_str__)
            
            blob_client = blob_service_client.get_blob_client(container=__container_name__, blob=blob_url)
            
            # print("\Downloading to Local Storage as blob:\n\t" + blob_storage_url)
            
            # Upload the file
            file_name = os.path.join(download_file_location, download_file_name)
            with open(file_name, "wb") as local_blob:
                blob_data = blob_client.download_blob()
                blob_data.readinto(local_blob)
    
        except Exception as ex:
            print('Exception:')
            print(ex)
    