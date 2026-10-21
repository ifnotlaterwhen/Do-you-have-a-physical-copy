# set up DB here with .env
# define a class for the DB manager
# export two instances of the class, one per database

import mysql.connector, os
from dotenv import load_dotenv

load_dotenv()

class DB_manager:
    def __init__(self, database):
        self.config = config

    def get_connection(self):
        connection = None

        try:
            connection = mysql.connector.connect(**config)

            if connection.is_connected():
                print("Connection Established")
                return connection
            
            else:
                print("Connection Failed") 
    
        except mysql.connector.Error as e: 
            print(f"Connection Error: {e}") 
            return None

manager_instance = DB_manager()