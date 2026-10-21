# set up DB here with .env
# define a class for the DB manager
# export an instance of the class

import os, mysql.connector 
from dotenv import load_dotenv

load_dotenv()

class DB_manager:
    def __init__(self, database):
        self.config = {
            "host" : os.getenv("host"),
            "port" : os.getenv("port"),
            "user" : os.getenv("user"),
            "password" : os.getenv("password"),
            "database" : database
        }
        self.connection = None

    def get_connection(self):
        

        try:
            self.connection = mysql.connector.connect(**self.config)

            if self.connection.is_connected():
                print("Connection Established")
                return self.connection
            
            else:
                print("Connection Failed") 
    
        except mysql.connector.Error as e: 
            print(f"Connection Error: {e}") 
            return None

    def close_connection(self):
        if self.connection and self.connection.is_connected(): 
            self.connection.close()
            print("Connection Closed")

manager_instance = DB_manager("database_name")