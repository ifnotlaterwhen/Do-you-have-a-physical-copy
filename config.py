# set up DB here with .env
# define a class for the DB manager
# export an instance of the class

import os, mysql.connector 
from dotenv import load_dotenv

load_dotenv()

class DB_manager:
    def __init__(self):
        self.config = {
            "host" : os.getenv("DB_HOST"),
            "port" : os.getenv("DB_PORT"),
            "user" : os.getenv("DB_USER"),
            "password" : os.getenv("DB_PW")
        }
        self.connection = None

    def get_connection(self):
        
        try:
            self.connection = mysql.connector.connect(**self.config)

            if self.connection.is_connected():
                print("Connection Established")
                return self.connection
            
            else:
                raise RuntimeError("Connection Failed")

        except mysql.connector.Error as e: 
            raise RuntimeError(f"Connection failed: {e}")

    def close_connection(self):
        if self.connection and self.connection.is_connected(): 
            self.connection.close()
            print("Connection Closed")
