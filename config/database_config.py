"""
Neuro_sync -Database configuration
SQLite database setting and connection parameters.
"""

import sqlite3
from pathlib import Path
from .settings import DATA_DIR, DATABASE_PATH


#DATABASE SETTINGS
class DatabaseConfig:
    #Main database path
    DATABASE_PATH = DATABASE_PATH

    #Connection settings
    TIMEOUT = 30.0
    CHECK_SAME_THREAD = False # Allows multi threading access