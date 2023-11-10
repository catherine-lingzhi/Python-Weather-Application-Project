"""
Description: Final Project Part 2 -Database
Date: 2023-11-09
Usage: Create a context manager module DBCM class to manage the database connection.
Group 7: Lingzhi Luo and Alem Bade Bene
"""
import sqlite3

class DBCM:
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None
        self.cursor = None

    def __enter__(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type is not None:
            self.conn.rollback() 
        else:
            self.conn.commit()  

        self.cursor.close()
        self.conn.close()