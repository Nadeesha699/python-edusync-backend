import mysql.connector

def get_db_connection():
   connection = mysql.connector.connect(
        host="localhost",
        username="root",
        password="",
        database="edusync_ict_db"
    )
   return connection