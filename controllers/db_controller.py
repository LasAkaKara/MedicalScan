import sqlite3
import os
import logging
import json

class DatabaseController:
    def __init__(self, db_name='app.db'):
        self.db_name = db_name
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """Connect to the database"""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.cursor = self.conn.cursor()
            logging.debug(f"Connected to database {self.db_name}")
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
    
    def create_tables(self):
        """Create necessary tables if they don't exist"""
        try:
            # Users table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Prescriptions table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS prescriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    image_path TEXT NOT NULL,
                    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    title TEXT,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # Settings table
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT
                )
            ''')
            
            self.conn.commit()
            logging.debug("Database tables created successfully")
        except sqlite3.Error as e:
            logging.error(f"Error creating tables: {e}")
    
    def execute(self, query, params=()):
        """Execute a query with parameters"""
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            logging.error(f"Error executing query: {e}")
            return False
    
    def fetch_one(self, query, params=()):
        """Fetch one result from a query"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            logging.error(f"Error fetching data: {e}")
            return None
    
    def fetch_all(self, query, params=()):
        """Fetch all results from a query"""
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error fetching data: {e}")
            return []
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
            logging.debug("Database connection closed") 
    