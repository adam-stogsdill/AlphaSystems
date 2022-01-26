import os
import pyodbc
import json
from azure.storage.blob import BlobServiceClient, ContainerClient, __version__
from azure.storage.blob.aio import BlobClient
import mysql.connector
from mysql.connector import errorcode

__container_name__ = None
__connection_str__ = None

class DatabaseHandler(object):
    
    def __init__(self, json_file_location: str):
        self.conn = None
        self.cursor = None
        self.connect(json_file_location=json_file_location)
        self.is_alive = True
    
    def connect(self, json_file_location: str):
        
        with open(json_file_location) as f:
            api_information = json.load(f)
    
        print(api_information)

        server = api_information['server']
        database = api_information['database']
        username = api_information['username']
        password = api_information['password']
        driver= api_information['driver']
        port = api_information['port']
        connstr = 'DRIVER='+driver+';SERVER='+server+';PORT='+port+';DATABASE='+database+';UID='+username+';PWD='+ password

        try:
            self.conn = pyodbc.connect(connstr)
            self.cursor = self.conn.cursor()
            return True

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("INVALID USERNAME AND/OR PASSWORD")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print(f"{database} DOES NOT EXIST")
            else:
                print(err)
    
    def get_table(self, table_name: str, return_as_dict: bool):
        
        sql_statement = f"SELECT * FROM {table_name};"
        # First execute the SELECT statement
        self.cursor.execute(sql_statement)
        
        # Then fetch the information from the cursor
        rows = self.cursor.fetchall()
        
        column_names = [column_tuple[0] for column_tuple in self.cursor.description]
        
        if return_as_dict:
            result_dict = {}
            for cn in column_names:
                result_dict[cn] = []
            
            num_columns = len(column_names)
            for row in rows:
                for col in range(num_columns):
                    result_dict[column_names[col]].append(row[col])
                    
            return column_names, result_dict
            
        return column_names, rows
        
    def clean(self):
        self.conn.commit()
        self.cursor.close()
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
    
    def __del__(self):
        c = self.conn
        print(f"Disconnecting {c}")
        self.clean()