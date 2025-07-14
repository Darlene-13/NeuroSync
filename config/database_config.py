"""
Database configuration  settings for the application.
"""

import sqlite3
from pathlib import Path
from .settings import DATABASE_PATH, APP_MODE, AppModes

#DATABASE SETTINGS
class DatabaseConfig:
    # Main database file
    DATABASE_PATH = DATABASE_PATH

    #Connection settings
    TIMEOUT = 30.0
    CHECK_SAME_THREAD = False

    #SQLite pragrams for performance and reliability
    PRAGMAS = {
        "journal_mode": "WAL", # write ahead logging for better accuracy
        "synchronous": "NORMAL", #Balance between safety and speed
        "cache_size": "10000",# 10MB Cache
        "temp_store": "memory", #Store temporary tables in memory
        "mmap_size": "268435456", # 256 memory_mapped I/0
        "foreign_keys": "ON", # Enalbe foreign key contraints
        "auto_vacuum": "FULL"
    }

    # Development vs production settings
    if APP_MODE == AppModes.DEVELOPMENT:
        PRAGMAS["synchronous"] = "OFF"  # Faster writes in development
    elif APP_MODE == App.Modes.PRODUCTION:
        PRAGMAS["synchronous"] = "FULL"  # Full safety in production


#CONNECTION HELPERS 
def get_connection_string():
    "'Get SQLite connection string for the database."
    return f"sqlite:///{DATABASE_PATH}"

def get_raw_connection():
    """ Get raw sqlite3 connection with optimized settings"""
    conn = sqlite3.connect(
        DATABASE_PATH
        timeout=DatabaseConfig.TIMEOUT 
        check_same_thread=DatabaseConfig.CHECK_SAME_THREAD
    )

    # Apply for pragmas for performance
    for pragma, value in DatabaseConfig.PRAGMAS.items():
        conn.execute(f" PRAGMA {pragma} = {value}"
                     )
        
    # Enable row factory for dict like access
    conn.row_factory = sqlite3.Row

    return conn

def apply_pragmas(conn):
    