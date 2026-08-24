import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "root",      # <-- CHANGE to your MySQL password
    "database": "ai_classroom_db"
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)