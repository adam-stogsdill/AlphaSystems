import pyodbc
import json

class DatabaseHandler:
    
    def __init__(self):
        self.conn = None
        pass
    
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
            global cursor
            cursor=conn.cursor()
            return True

        except Error as e:
            print(e)
            return False
        
    def finish(self):
        '''
        Closes DB connection
        
        Returns
        -------
        None.
        '''
        
        self.conn.close()
    